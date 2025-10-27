from google.adk.agents.llm_agent import Agent
import pandas as pd

# Mock tool implementation
def get_random_measurement(patient: str) -> dict:
    """Returns a random measurement of the patient."""
    data = pd.read_csv("Data\\post-operative-data-with-names.csv")
    # 1. Filter for the patient's data (case-insensitive partial match)
    data_filtered_parial = data[data['Name'].str.contains(patient, case=False, na=False)]
    
    # Check if patient was found
    if data_filtered_parial.empty:
        return {"status": "error", "message": f"Patient '{patient}' not found."}
    
    df_subset = data_filtered_parial.iloc[:, :-2]
    all_values_series = df_subset.stack()
    random_value = all_values_series.sample(n=1)
    measurement_type = random_value.index[0][1]
    value = random_value.iloc[0]
    return {"status": "success", "measurement_type": measurement_type, "value": value}

def get_specific_measurement(patient: str, measurement_type: str):
    """
    Returns a specific measurement of the patient, allowing for inexact 
    matching of the measurement_type
    """
    data = pd.read_csv("Data\\post-operative-data-with-names.csv")
    
    # 1. Filter for the patient's data (case-insensitive partial match)
    data_filtered_parial = data[data['Name'].str.contains(patient, case=False, na=False)]
    
    # Check if patient was found
    if data_filtered_parial.empty:
        return {"status": "error", "message": f"Patient '{patient}' not found."}

    # 2. Find the column header that matches the measurement_type inexactly
    #    We use 'case=False' for case-insensitivity and 'na=False'
    #    The 'measurement_type' argument will be used as a pattern (e.g., 'Lo2')
    matching_columns = [
        col for col in data_filtered_parial.columns 
        if measurement_type.lower() in col.lower()
    ]

    # 3. Handle matching results
    if not matching_columns:
        # No matching measurement type found
        return {"status": "error", "message": f"Measurement type matching '{measurement_type}' not found for patient '{patient}'."}
    
    if len(matching_columns) > 1:
        # Multiple columns match the partial search term
        # For simplicity, we can choose the first match, but a better approach
        # in a real application might be to ask for clarification.
        # Choosing the first match:
        actual_measurement_type = matching_columns[0]
        print(f"**Note:** Multiple measurements matched '{measurement_type}'. Using '{actual_measurement_type}'.")
    else:
        # Exactly one match found
        actual_measurement_type = matching_columns[0]
    
    # 4. Get the value using the actual, full column name
    value = data_filtered_parial[actual_measurement_type].iloc[0]
    
    return {"status": "success", "measurement_type": actual_measurement_type, "value": value}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Can get a measurement of a patient",
    instruction="You are a helpful nurse that can do a measurement of a patient. Use the 'get_measurement' tool to get a random measurement of the patient. Use the 'get_specific_measurement' tool to get a specific type of measurement of the patient. **Your final answer MUST be a valid JSON object** with keys 'measurement_type', and 'value'.",
    tools=[get_random_measurement, get_specific_measurement],
    sub_agents=[],
)


