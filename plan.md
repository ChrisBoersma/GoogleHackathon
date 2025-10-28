# Plan for the Doctor Agent (Input Parameter Approach)

## 1. Goal

To refactor the `Doctor` agent to accept the patient's name as a direct input parameter, simplifying the workflow and making it more robust. This eliminates the need for a conversational intake step.

## 2. High-Level Workflow

1.  **Invocation:** The user will invoke the `Doctor` agent and provide the patient's name as an argument.
2.  **Diagnostic Loop:** The agent will immediately start the diagnostic process using the provided name.
3.  **Patient Communication:** Once a confident diagnosis is reached, the agent will generate a message for the patient.

## 3. Agent Composition

The `PatientIntake_agent` is no longer needed.

*   **`DoctorWorkflow` (`SequentialAgent`):** The root agent will be a simple sequence.
    1.  `DataGatheringLoop`
    2.  `PatientCommunicationAgent`

*   **`DataGatheringLoop` (`LoopAgent`):** The loop for iterative diagnosis.
    1.  `NurseAgent`
    2.  `DataScientistAnalysisAgent`
    3.  `CheckCondition` (90% threshold)
    4.  `DataScientistMetricAgent`

## 4. Implementation Steps

1.  **Update `plan.md`:** Document the new approach (this file).
2.  **Modify `Doctor/agent.py`:**
    a.  Remove the `PatientIntake_agent` from the workflow.
    b.  Modify the `DoctorWorkflow` to accept the patient's name as an input and place it in the session state so the `NurseAgent` can access it.