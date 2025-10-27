from google.adk.agents.llm_agent import Agent
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import json

def get_train_data() -> str:
    """Returns the training data as a JSON string."""
    data = pd.read_csv("Data/post-operative-data.csv")
    return data.to_json()

def predict_using_decision_tree(data: str, patient_data: str) -> str:
    """Creates a decision tree from the given data and returns the classifier and encoders."""

    df = pd.read_json(data)
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
    """Uses the decision tree to make a prediction."""
    patient_df = pd.read_json(patient_data)
    for col, le in encoders.items():
        if col in patient_df.columns and patient_df[col].dtype == 'object':
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
    Return the prediction
    """,
    tools=[create_record,get_train_data,predict_using_decision_tree],
    sub_agents=[],
)
