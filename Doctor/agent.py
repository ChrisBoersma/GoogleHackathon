from google.adk.agents import LoopAgent, LlmAgent, BaseAgent, SequentialAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator

from Doctor.sub_agents.PatientCommunication.agent import PatientCommunication_agent
from Nurse_agent.agent import root_agent as Nurse_LLMAgent
from datascientist_agent.agent import create_record,get_train_data,predict_using_decision_tree,drop_columns_without_data

# Data Scientist agent for analysis
data_scientist_analysis_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='DataScientistAnalysisAgent',
    instruction='''
    You are a data scientist. You will be given patient data.
    Analyze the data and provide a `ConfidenceScore` for your decision.
    The `ConfidenceScore` should be a number between 0 and 100.
    Also provide the `Decision` which can be "in-patient" or "out-patient".
    Your output should be in the format:
    ConfidenceScore: [score]
    Decision: [decision]
    ''',
    tools=[create_record,get_train_data,predict_using_decision_tree,drop_columns_without_data],
)

# Data Scientist agent for suggesting next metric
data_scientist_metric_agent = LlmAgent(
    model='gemini-1.5-flash',
    name='DataScientistMetricAgent',
    instruction='''
    You are a data scientist. You will be given patient data and a low `ConfidenceScore`.
    Your task is to determine the next best metric to collect to improve the confidence score.
    Your output should be the name of the metric to collect.
    ''',
    tools=[create_record,get_train_data,predict_using_decision_tree,drop_columns_without_data],
)


# Custom agent to check for the termination condition
class CheckCondition(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        confidence_score = ctx.session.state.get("ConfidenceScore", 0)
        is_done = (confidence_score >= 90)
        yield Event(author=self.name, actions=EventActions(escalate=is_done))

# Instantiate the checker
checker = CheckCondition(name="ConfidenceChecker")

# Create the LoopAgent for iterative data gathering and analysis
data_gathering_loop = LoopAgent(
    name="DataGatheringLoop",
    max_iterations=10,  # Safety break
    sub_agents=[
        Nurse_LLMAgent,
        data_scientist_analysis_agent,
        checker,
        data_scientist_metric_agent,
    ]
)

# Define the root agent for the entire workflow
root_agent = SequentialAgent(
    name='DoctorWorkflow',
    sub_agents=[
        data_gathering_loop,
        PatientCommunication_agent,
    ]
)
