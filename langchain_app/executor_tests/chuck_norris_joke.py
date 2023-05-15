from langchain.agents import initialize_agent, AgentType
from langchain_app.models.vicuna_request_llm import VicunaLLM

from code_it.models import build_llama_base_llm
from code_it.langchain.code_it_tool import CodeItTool
from code_it.task_executor import TaskExecutionConfig

llm = VicunaLLM()
config = TaskExecutionConfig()
print(config)
config.install_dependencies = False
config.execute_code = True
code_editor = CodeItTool(build_llama_base_llm, config)

tools = [
    code_editor.build_execute_task(),
]

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    """

Remember to use the following format:
Action: <>
Action Input:
<>

Question: The endpoint https://api.chucknorris.io/jokes/random returns a joke about Chuck Norries

1. Write a python Program that fetches a joke from this endpoint.
2. Extract the joke from the response. Access the 'value' in the JSON to extract it.
3. Prints the joke to the screen.
"""
)