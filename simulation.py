import pandas as pd
import argparse
import random
import time

# --- Mock Implementations of Sub-Agents ---

class MockNurse:
    """A mock nurse that holds a patient's data and provides it on request."""
    def __init__(self, patient_record):
        self.patient_record = patient_record
        # Clean up column names by stripping whitespace
        self.patient_record.index = self.patient_record.index.str.strip()

    def run(self, prompt):
        print(f"  [Nurse] Received request: \"{prompt}\"")
        if "get first piece of data" in prompt:
            # Return a primary, important metric first
            return {"L-O2": self.patient_record["L-O2"]}
        elif "get" in prompt:
            metric_name = prompt.split("get ")[1].strip()
            if metric_name in self.patient_record:
                return {metric_name: self.patient_record[metric_name]}
            else:
                return {metric_name: "unknown"}

class MockDataScientist:
    """A mock data scientist that makes predictions based on available metrics."""
    def run(self, metrics=None, prompt=None):
        if prompt and "What single metric" in prompt:
            print("  [Data Scientist] Received request for metric suggestion.")
            # Suggest the next most important metric that is currently missing.
            required_metrics = ["L-CORE", "L-SURF", "L-BP", "SURF-STBL", "CORE-STBL", "BP-STBL", "COMFORT"]
            for m in required_metrics:
                if m not in metrics:
                    print(f"  [Data Scientist] Suggesting: {m}")
                    return {"metric_name": m}
            return {"metric_name": "none"} # Should not happen in a good run

        if metrics:
            print(f"  [Data Scientist] Received metrics for analysis: {metrics}")
            num_metrics = len(metrics)
            
            # Simulate confidence increasing with more data
            confidence = min(0.5 + (num_metrics * 0.15), 1.0)
            
            # A simple rule for the decision
            decision = "A" # Default to Admit
            if "L-O2" in metrics and metrics["L-O2"] == "excellent":
                decision = "S" # Send home if O2 is great
            if "CORE-STBL" in metrics and metrics["CORE-STBL"] == "unstable":
                decision = "I" # ICU if core is unstable
            
            print(f"  [Data Scientist] Prediction: {decision}, Confidence: {confidence:.2f}")
            return {"Decision": decision, "ConfidenceScore": confidence}

class MockPatientCommunication:
    """A mock communication agent that formats a message for the patient."""
    def run(self, patient_name, decision):
        print("  [Communication Agent] Generating message...")
        message_map = {
            "S": f"Hello {patient_name}, the doctor has reviewed your results and you are cleared to go home. Please get some rest!",
            "A": f"Hello {patient_name}, we'd like to admit you to the hospital for some further observation. A nurse will be with you shortly.",
            "I": f"Hello {patient_name}, we need to move you to the Intensive Care Unit for closer monitoring. You are in good hands."
        }
        return message_map.get(decision, "No decision message available.")

# --- Simulation of the Doctor Agent's Logic ---

def simulate_doctor_agent_run(patient_name, nurse_agent, data_scientist_agent, communication_agent):
    """Simulates the execution flow of the Doctor_agent based on its protocol."""
    print("  [Doctor] Starting consultation...")
    collected_metrics = {}

    # 1. Initial Data
    initial_data = nurse_agent.run(prompt="get first piece of data")
    collected_metrics.update(initial_data)
    time.sleep(0.5) # pause for readability

    # Start Iteration Loop
    for i in range(10): # Add a safety break to prevent infinite loops
        # 2. Analyze Data
        analysis = data_scientist_agent.run(metrics=collected_metrics.copy())
        confidence = analysis.get("ConfidenceScore", 0)
        decision = analysis.get("Decision")
        time.sleep(0.5)

        # 3. Decision Point
        if confidence > 0.95:
            print("  [Doctor] Confidence threshold met. Exiting loop.")
            break

        print("  [Doctor] Confidence low. Requesting more data.")
        # 4. Get Next Metric Name
        suggestion = data_scientist_agent.run(prompt="What single metric should I collect next?")
        next_metric_name = suggestion.get("metric_name")
        time.sleep(0.5)
        
        if next_metric_name == "none":
            print("  [Doctor] No more metrics to collect. Exiting loop.")
            break

        # 5. Request Specific Value
        new_metric = nurse_agent.run(prompt=f"get {next_metric_name}")
        collected_metrics.update(new_metric)
        time.sleep(0.5)
    
    # 6. Communicate to Patient
    final_message = communication_agent.run(patient_name=patient_name, decision=decision)
    print("  [Doctor] Consultation finished.")
    return final_message

# --- Main Simulation Runner ---

def run_simulation(num_patients):
    """Main function to run the patient processing simulation."""
    try:
        patient_data = pd.read_csv('Data/post-operative-data-with-names.csv')
    except FileNotFoundError:
        print("Error: The data file 'Data/post-operative-data-with-names.csv' was not found.")
        return

    if num_patients > len(patient_data):
        print(f"Warning: Requested {num_patients} patients, but only {len(patient_data)} are available. Running for all patients.")
        num_patients = len(patient_data)
    
    selected_patients = patient_data.sample(n=num_patients)

    print(f"--- Starting simulation for {num_patients} patient(s) ---")

    for index, patient in selected_patients.iterrows():
        patient_name = patient['Name'].strip()
        print(f"\n>>> Processing patient: {patient_name} <<<")
        
        # Instantiate mock agents for this patient
        nurse = MockNurse(patient)
        data_scientist = MockDataScientist()
        communicator = MockPatientCommunication()

        # Run the simulated pipeline
        final_patient_message = simulate_doctor_agent_run(
            patient_name=patient_name,
            nurse_agent=nurse,
            data_scientist_agent=data_scientist,
            communication_agent=communicator
        )
        print(f"\n--- Final Message for {patient_name} ---\n{final_patient_message}\n------------------------------------")
        time.sleep(1)

    print("\n--- Simulation complete ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simulation of the Doctor Agent pipeline.")
    parser.add_argument("-n", "--num_patients", type=int, default=1, help="The number of patients to simulate.")
    args = parser.parse_args()
    
    run_simulation(args.num_patients)