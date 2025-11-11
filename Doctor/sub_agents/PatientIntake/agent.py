from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

import os
modelname = "azure/gpt-4.1"
llmModel = LiteLlm(model=modelname)


PatientIntake_agent = LlmAgent(
    model=llmModel,
    name='PatientIntakeAgent',
    instruction='''
    You are a friendly patient intake specialist.
    Your goal is to greet the user and ask for the patient's name.
    Once you have the name, your only output should be the patient's name.
    For example, if the user says "The patient is John Smith", you should output "John Smith".
    '''
)