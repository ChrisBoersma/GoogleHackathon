from google.adk.agents.llm_agent import Agent
import pandas as pd

# Mock tool implementation
def get_random_measurement(patient: str) -> dict:
    """Returns a random measurement of the patient."""
    data = pd.read_csv("Data\\post-operative-data-with-names.csv")
    data_filtered_parial = data[data['Name'].str.contains(patient, case=False, na=False)]
    df_subset = data_filtered_parial.iloc[:, :-2]
    all_values_series = df_subset.stack()
    random_value = all_values_series.sample(n=1)
    measurement_type = random_value.index[0][1]
    value = random_value.iloc[0]
    return {"status": "success", "measurement_type": measurement_type, "value": value}

def get_specific_measurement(patient: str, measurement_type: str):
    """Returns a specific measurement of the patient."""
    data = pd.read_csv("Data\\post-operative-data-with-names.csv")
    data_filtered_parial = data[data['Name'].str.contains(patient, case=False, na=False)]
    data_subset = data_filtered_parial[measurement_type]
    value = data_subset.iloc[0]
    return {"status": "success", "measurement_type": measurement_type, "value": value}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Can get a measurement of a patient",
    instruction="You are a helpful nurse that can do a measurement of a patient. Use the 'get_measurement' tool to get a random measurement of the patient. Use the 'get_specific_measurement' tool to get a specific type of measurement of the patient. **Your final answer MUST be a valid JSON object** with keys 'measurement_type', and 'value'.",
    tools=[get_random_measurement, get_specific_measurement],
    sub_agents=[],
)


