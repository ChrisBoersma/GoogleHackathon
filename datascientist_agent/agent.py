from google.adk.agents.llm_agent import Agent
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import os

def get_train_data(filename: str) -> str:
    """Open a csv file and saves the training data to a pickle file and returns the path."""
    data = pd.read_csv("./Data/"  + filename)
    pickle_path = f"/home/bazarow/Projects/GoogleHackathon/temp_pickle_data/{filename.split('/')[-1].split('.')[0]}.pickle"
    data.to_pickle(pickle_path)
    return pickle_path

def drop_columns_without_data(data_path:str, patient_data:str, target_column: str) -> str:
    """Filters the data to only keep columns present in patient_data and the target column."""
    df = pd.read_pickle(data_path)
    patient_df = pd.read_json(patient_data)
    
    patient_columns = patient_df.columns.tolist()
    columns_to_keep = patient_columns + [target_column]
    
    # Ensure only existing columns are selected
    existing_columns_to_keep = [col for col in columns_to_keep if col in df.columns]
    
    filtered_df = df[existing_columns_to_keep]
    filtered_data_path = f"/home/bazarow/Projects/GoogleHackathon/temp_pickle_data/filtered_{data_path.split('/')[-1]}"
    filtered_df.to_pickle(filtered_data_path)
    return filtered_data_path

def predict_using_decision_tree(data_path: str, patient_data: str, target_column: str) -> str:
    """Creates a decision tree from the given data and returns the prediction. Only use this function if you have made sure the data and the patient data have the same labelled columns"""
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=None, random_state=42)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    
    patient_df = pd.read_json(patient_data)
    for col, le in encoders.items():
        if col in patient_df.columns and patient_df[col].dtype == 'object':
            known_labels = le.classes_
            # Replace unseen labels with the first known label
            patient_df[col] = patient_df[col].apply(lambda x: x if x in known_labels else known_labels[0])
            patient_df[col] = le.transform(patient_df[col])
    prediction = clf.predict(patient_df)
    if target_column in encoders:
        le = encoders[target_column]
        prediction = le.inverse_transform(prediction)
    return str(prediction[0])

def create_record_patient(name : str) -> str:
    """Creates a patient record and returns it as a JSON string."""
    patient_data = pd.DataFrame({
        'L-CORE': ['low'],
        'L-SURF': ['low'],
        'L-O2': ['excellent'],
        'L-BP': ['mid'],
        'SURF-STBL': ['stable']
    })
    return patient_data.to_json()

def create_record_animal() -> str:
    """Creates an animal record and returns it as a JSON string."""
    animal_data = pd.DataFrame({
        'hair': [1],
        'feathers': [0],
        'eggs': [0],
        'milk': [1],
        'airborne': [0],
        'aquatic': [0],
        'predator': [1],
        'toothed': [1],
        'backbone': [1],
        'breathes': [1],
        'venomous': [0],
        'fins': [0],
        'legs': [4],
        'tail': [1],
        'domestic': [0],
        'catsize': [1]
    })
    return animal_data.to_json()

def create_record_giraffe() -> str:
    """Creates an animal record for a giraffe and returns it as a JSON string."""
    animal_data = pd.DataFrame({
        'hair': [1],
        'feathers': [0],
        'eggs': [0],
        'milk': [1],
        'airborne': [0],
        'aquatic': [0],
        'predator': [0],
        'toothed': [1],
        'backbone': [1],
        'breathes': [1],
        'venomous': [0],
        'fins': [0],
        'legs': [4],
        'tail': [1],
        'domestic': [0],
        'catsize': [0]
    })
    return animal_data.to_json()

def get_columns_name(file_path: str) -> list[str]:
    """Given a filepath for a pickle file, returns the corresponding column names."""
    df = pd.read_pickle(file_path)
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
    You get a record which you can get by name. Use the create_record functions to get the values for the record. 
    You can also be asked to predict a certain column. 
    Check which dataset you need with get_column_names. If the column name is not a 1 on 1 match, you can decide which column is the best fit. 
    You can also to determine how the prediction column is called.
    Use this data to make a prediction using the filled in record for the patient.
    Return the prediction. Show your steps and thought process.
    """,
    tools=[create_record_patient, create_record_animal, create_record_giraffe, get_train_data,predict_using_decision_tree,drop_columns_without_data, get_columns_name, list_data_files],
    sub_agents=[],
)
