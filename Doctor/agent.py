from google.adk.agents.llm_agent import Agent
from Doctor.sub_agents.PatientCommunication.agent import PatientCommunication_agent
from Nurse_agent.agent import root_agent as Nurse_LLMAgent
from datascientist_agent.agent import root_agent as Data_Scientist_LLMAgent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='Doctor_agent',
    description="Talks with patients and calls sub agents",
    instruction=
    """
    You are a Doctor agent. Your goal is to determine if a patient should be in the "in-patient" or "out-patient" program.

    1.  You will be given the patient's **Name**.
    2.  First, call the `Nurse_LLMAgent` to get the initial patient data.
    3.  Then, repeatedly call the `Data_Scientist_LLMAgent` to analyze the data and get a `ConfidenceScore`.
    4.  If the `ConfidenceScore` is low, call the `Data_Scientist_LLMAgent` again to ask for the next metric to collect. Then call the `Nurse_LLMAgent` to get the value for that metric.
    5.  Repeat step 3 and 4 until the `ConfidenceScore` is high (e.g., > 95%).
    6.  Once the `ConfidenceScore` is high, call the `PatientCommunication_agent` with the final `Decision` and the patient's `Name` to generate a message for the patient.
    7.  Your final output must be the message from the `PatientCommunication_agent`.
    """,
    tools=[],
    sub_agents=[PatientCommunication_agent, Nurse_LLMAgent, Data_Scientist_LLMAgent],
)