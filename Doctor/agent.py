from google.adk.agents import LoopAgent, LlmAgent, SequentialAgent
from google.adk.events import Event, EventActions
from typing import AsyncGenerator

from Doctor.sub_agents.PatientCommunication.agent import PatientCommunication_agent
from Nurse_agent.agent import root_agent as Nurse_LLMAgent
from datascientist_agent.agent import root_agent as DataScientist_agent

# Agent to prepare the input for the DataScientist_agent
prepare_ds_input = LlmAgent(
    model='gemini-2.5-flash',
    name='PrepareDSInput',
    instruction='''Take the input you receive and append the following text to it: "\n\nPredict the 'adm-decs' column."'''
)

# Agent to check the termination condition
checker = LlmAgent(
    model='gemini-2.5-flash',
    name='ConfidenceChecker',
    instruction='''You will be given a string containing a prediction and a certainty percentage, like "Prediction: A, Certainty: 95.00%".
    Your task is to check if the certainty is 60% or higher.
    - If the certainty is 60% or higher, you MUST output **ONLY** the word "STOP".
    - Otherwise, output the original text you received, unchanged.'''
)

# Create the LoopAgent for iterative data gathering and analysis
data_gathering_loop = LoopAgent(
    name="DataGatheringLoop",
    max_iterations=1,  # Safety break
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
