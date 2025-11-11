from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

import os
LITELLM_MODEL = os.environ.get('LITELLMAZUREMODEL', "openai/gpt-4.1")
LITELLM_API_KEY = os.environ.get('LITELLMAZUREAPIKEY')
LITELLM_API_BASE = os.environ.get('LITELLMAZUREAPIBASE')

llmModel = LiteLlm(
  model=LITELLM_MODEL,
  api_key=LITELLM_API_KEY,
  api_base=LITELLM_API_BASE
)


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