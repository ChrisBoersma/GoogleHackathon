from google.adk.agents.llm_agent import Agent
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle

def get_train_data() -> str:
    """Saves the training data to a pickle file and returns the path."""
    data = pd.read_csv("Data/post-operative-data.csv")
    pickle_path = "/home/bazarow/Projects/GoogleHackathon/Data/post-operative-data.pickle"
    data.to_pickle(pickle_path)
    return pickle_path

def drop_columns_without_data(data_path:str, patient_data:str) -> str:
    """Filters the data to only keep columns present in patient_data and 'decision ADM-DECS'."""
    df = pd.read_pickle(data_path)
    patient_df = pd.read_json(patient_data)
    
    patient_columns = patient_df.columns.tolist()
    columns_to_keep = patient_columns + ['decision ADM-DECS']
    
    # Ensure only existing columns are selected
    existing_columns_to_keep = [col for col in columns_to_keep if col in df.columns]
    
    filtered_df = df[existing_columns_to_keep]
    filtered_data_path = "/home/bazarow/Projects/GoogleHackathon/Data/filtered_post-operative-data.pickle"
    filtered_df.to_pickle(filtered_data_path)
    return filtered_data_path

def predict_using_decision_tree(data_path: str, patient_data: str) -> str:
    """Creates a decision tree from the given data and returns the prediction."""
    df = pd.read_pickle(data_path)
    df = df.replace('?', np.nan)
    df = df.dropna()
    encoders = {}
    for col in df.columns:
        if df[col].dtype == 'object':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le
    X = df.drop('decision ADM-DECS', axis=1)
    y = df['decision ADM-DECS']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
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
    return str(prediction)

def create_record(name : str) -> str:
    """Creates a patient record and returns it as a JSON string."""
    patient_data = pd.DataFrame({
        'L-CORE': ['low'],
        'L-SURF': ['low'],
        'L-O2': ['excellent'],
        'L-BP': ['mid'],
        'SURF-STBL': ['stable'],
        'CORE-STBL': ['stable'],
        'BP-STBL': ['stable'],
        'COMFORT': [15]
    })
    return patient_data.to_json()


#todo state
root_agent = Agent(
    model='gemini-2.5-flash',
    name='datascientist_agent',
    description="Answers questions about a dataset",
    instruction="""You are a datascientist in an hospital. 
    You get a patient with name. Use the create_record to get the values for the patient.
    There is a dataset which you can get with get_train_data. Use this data to make a prediction using the filled in record for the patient.
    Return the prediction. Show your steps and thought process.
    """,
    tools=[create_record,get_train_data,predict_using_decision_tree,drop_columns_without_data],
    sub_agents=[],
)
