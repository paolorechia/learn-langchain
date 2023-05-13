from langchain.agents import Tool, initialize_agent, AgentType
from langchain_app.models.vicuna_request_llm import VicunaLLM
from code_it.langchain.code_it_tool import CodeItTool

llm = VicunaLLM()

code_editor = CodeItTool(VicunaLLM)

tools = [
    code_editor.build_execute_task(),
]

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    """
Your job is to plot an example chart using matplotlib. Create your own random data.
Run this code only when you're finished.
DO NOT add code and run into a single step.
"""
)