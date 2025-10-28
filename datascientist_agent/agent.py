from google.adk.agents.llm_agent import Agent
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import os
from io import StringIO
import json

def get_train_data(filename: str) -> str:
    """Open a csv file and saves the training data to a pickle file and returns the path."""
    data = pd.read_csv("./Data/"  + filename)
    pickle_path = f"./temp_pickle_data/{filename.split('/')[-1].split('.')[0]}.pickle"
    data.to_pickle(pickle_path)
    return pickle_path

def drop_columns_without_data(data_path:str, patient_data:str, target_column: str) -> str:
    """Filters the data to only keep columns present in patient_data and the target column."""
    df = pd.read_pickle(data_path)
    try:
        patient_df = pd.read_json(StringIO(patient_data))
    except ValueError as e:
        if "If using all scalar values, you must pass an index" in str(e):
            patient_df = pd.DataFrame(json.loads(patient_data), index=[0])
        else:
            raise
    
    patient_columns = patient_df.columns.tolist()
    columns_to_keep = patient_columns + [target_column]
    
    # Ensure only existing columns are selected
    existing_columns_to_keep = [col for col in columns_to_keep if col in df.columns]
    
    filtered_df = df[existing_columns_to_keep]
    filtered_data_path = f"./temp_pickle_data/filtered_{data_path.split('/')[-1]}"
    filtered_df.to_pickle(filtered_data_path)
    return filtered_data_path

def predict_using_random_forest(data_path: str, patient_data: str, target_column: str) -> str:
    """Creates a random forest from the given data and returns the prediction and the certainty of the prediction. Only use this function if you have made sure the data and the patient data have the same labelled columns"""
    df = pd.read_pickle(data_path)
    df = df.replace('?', np.nan)
    df = df.dropna()
    encoders = {}
    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le
    X = df.drop(target_column, axis=1)
    y = df[target_column]

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, y)
    
    try:
        patient_df = pd.read_json(StringIO(patient_data))
    except ValueError as e:
        if "If using all scalar values, you must pass an index" in str(e):
            patient_df = pd.DataFrame(json.loads(patient_data), index=[0])
        else:
            raise
    for col, le in encoders.items():
        if col in patient_df.columns and patient_df[col].dtype == 'object':
            known_labels = le.classes_
            # Replace unseen labels with the first known label
            patient_df[col] = patient_df[col].apply(lambda x: x if x in known_labels else known_labels[0])
            patient_df[col] = le.transform(patient_df[col])
    
    prediction_encoded = clf.predict(patient_df)
    prediction_proba = clf.predict_proba(patient_df)
    
    certainty = np.max(prediction_proba)

    prediction = prediction_encoded
    if target_column in encoders:
        le = encoders[target_column]
        prediction = le.inverse_transform(prediction_encoded)

    return f"Prediction: {prediction[0]}, Certainty: {certainty:.2%}"

def create_record_patient(name: str) -> str:
    """Creates a patient record by name and returns it as a JSON string."""
    
    # Load the dataset
    df = pd.read_csv('./Data/post-operative-data-with-names.csv')
    
    # Correct column names by stripping leading/trailing spaces
    df.columns = df.columns.str.strip()
    
    # Find the patient by name
    # Case-insensitive search and stripping spaces from name column
    patient_row = df[df['Name'].str.strip().str.lower() == name.lower()]
    
    if not patient_row.empty:
        # Exclude 'decision ADM-DECS' and 'Name' columns
        patient_data = patient_row.drop(columns=['decision ADM-DECS', 'Name'])
        return patient_data.to_json()
    else:
        return f"No record found for name: {name}"

def create_record_animal_by_name(name: str) -> str:
    """Creates an animal record by name and returns it as a JSON string."""
    
    # Load the dataset
    df = pd.read_csv('./Data/zoo.csv')
    
    # Correct column names by stripping leading/trailing spaces
    df.columns = df.columns.str.strip()
    
    # Find the animal by name
    # Case-insensitive search and stripping spaces from name column
    animal_row = df[df['animal_name'].str.strip().str.lower() == name.lower()]
    
    if not animal_row.empty:
        # Exclude 'class_type' and 'animal_name' columns
        animal_data = animal_row.drop(columns=['class_type', 'animal_name'])
        return animal_data.to_json()
    else:
        return f"No record found for name: {name}"



def get_columns_name(file_path: str) -> list[str]:
    """Given a filepath for a pickle file, you can only access the pickle file if you have gotten the train data from the csv. returns the corresponding column names."""
    try:
        df = pd.read_pickle(file_path)
    except:
        return "first read the csv"
    return df.columns.tolist()

def list_data_files() -> list[str]:
    """Returns a list of filenames in the Data directory."""
    return os.listdir('./Data')


#todo state
root_agent = Agent(
    model='gemini-2.5-flash',
    name='datascientist_agent',
    description="Answers questions about a dataset",
    
    instruction="""You are a datascientist.
    You get a record.
    You can also be asked to predict a certain column. 
    Check which dataset you need with get_column_names. If the column name is not a 1 on 1 match, you can decide which column is the best fit. 
    If there is no target column given, ask for one.
    You can also to determine how the prediction column is called.
    Use this data to make a prediction using the filled in record for the patient.
    Return the prediction. Show your steps and thought process.
    """,
    tools=[get_train_data, predict_using_random_forest,drop_columns_without_data, get_columns_name, list_data_files],
    sub_agents=[],
)
