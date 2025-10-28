import re
from google.adk.agents import LoopAgent, LlmAgent, SequentialAgent
from google.adk.events import Event, EventActions
from typing import AsyncGenerator

from google.adk.tools.tool_context import ToolContext

from Doctor.sub_agents.PatientCommunication.agent import PatientCommunication_agent
from Nurse_agent.agent import root_agent as Nurse_LLMAgent
from datascientist_agent.agent import root_agent as DataScientist_agent


# Agent to prepare the input for the DataScientist_agent
prepare_ds_input = LlmAgent(
    model='gemini-2.5-flash',
    name='PrepareDSInput',
    instruction='''Take the input you received using all previous dataentries collected by the nursing agent for this individual. Only use all measurements and append the following text to it: "\n\nPredict the 'adm-decs' column."'''
)

def exit_loop(tool_context: ToolContext):
  """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
  print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
  tool_context.actions.escalate = True
  # Return empty dict as tools should typically return JSON-serializable output
  return {}

# Agent to check the termination condition
checker = LlmAgent(
    model='gemini-2.5-flash',
    name='ConfidenceChecker',
    instruction='''You will be given a string containing a prediction and a certainty percentage, like "Prediction: A, Certainty: 95.00%".
    Your task is to check if the certainty is 90% or higher.
    - If the certainty is 90% or higher,     You MUST call the 'exit_loop' function. Do not output any text.
    - If there is no certainty, output the original text and continue the loop!''',
    tools=[exit_loop]

)


# Create the LoopAgent for iterative data gathering and analysis
data_gathering_loop = LoopAgent(
    name="DataGatheringLoop",
    max_iterations=5,  # Safety break
    sub_agents=[
        Nurse_LLMAgent,
        prepare_ds_input,
        DataScientist_agent,
        checker,
    ],
)





# Define the root agent for the entire workflow
root_agent = SequentialAgent(
    name='DoctorWorkflow',
    sub_agents=[
        data_gathering_loop,
        PatientCommunication_agent,
    ]
)
