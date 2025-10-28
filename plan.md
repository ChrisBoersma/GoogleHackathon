# Plan for the Doctor Agent

## 1. Project Goal

To create a `Doctor` agent that orchestrates a diagnostic workflow. The agent will interact with the user to get a patient's name, then iteratively gather and analyze patient data using sub-agents until a confident diagnosis is reached. Finally, it will generate a patient-friendly message with the outcome.

## 2. High-Level Workflow

1.  **Patient Intake:** The agent will start by asking the user for the patient's name.
2.  **Iterative Diagnosis Loop:** The agent will enter a loop that continues until the confidence score from the data scientist is 90% or higher.
    a.  **Get Metric:** On the first iteration, it will ask the `NurseAgent` for a random metric. On subsequent iterations, it will ask for a specific metric recommended by the `DataScientistMetricAgent`.
    b.  **Analyze Data:** The collected metric(s) will be passed to the `DataScientistAnalysisAgent` to get a prediction and a confidence score.
    c.  **Check Confidence:** If the score is below 90%, the `DataScientistMetricAgent` will be called to determine the next best metric to collect.
3.  **Patient Communication:** Once the loop terminates, the final prediction will be passed to the `PatientCommunicationAgent` to generate a message for the patient.

## 3. Agent Composition

*   **`DoctorWorkflow` (`SequentialAgent`):** The root agent that will manage the overall workflow.
    1.  `PatientIntakeAgent`
    2.  `DataGatheringLoop`
    3.  `PatientCommunicationAgent`

*   **`DataGatheringLoop` (`LoopAgent`):** The loop will be structured as follows to ensure the correct flow of data:
    1.  `NurseAgent`
    2.  `DataScientistAnalysisAgent`
    3.  `CheckCondition` (set to a 90% threshold)
    4.  `DataScientistMetricAgent`

## 4. Implementation Steps

1.  **Implement `Doctor/agent.py`:** Write the Python code for the `Doctor` agent, defining and composing the `DoctorWorkflow` and `DataGatheringLoop` as described above.
