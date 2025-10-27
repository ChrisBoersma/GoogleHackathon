from google.adk.agents.llm_agent import Agent
import pandas as pd

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

def get_data_patient(patient: str) -> dict:
    """Returns the data of a patient."""
    data = pd.read_csv("Data\\healthcare_dataset.csv")
    data_filtered_parial = data[data['Name'].str.contains(patient, case=False, na=False)]

    return {"status": "success", "patient": patient, "data": str(data_filtered_parial)}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Answers questions about a dataset",
    instruction="You are a helpful assistant that gets medical data of a certain patient from a dataset. Use the 'get_data_patient' tool to get the data of the patient.",
    tools=[get_data_patient],
    sub_agents=[],
)


