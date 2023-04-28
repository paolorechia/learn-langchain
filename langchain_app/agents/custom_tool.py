# This is currently broken, needs to be updated
from langchain.agents import Tool, AgentExecutor, ZeroShotAgent
from langchain import LLMChain
from langchain.tools.python.tool import PythonAstREPLTool
from langchain.tools.multi_line_human.tool import MultiLineHumanInputRun
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests


class CodeOracleInput(BaseModel):
    input_code: str = Field()


def call_code_endpoint(oracle_input: CodeOracleInput):
    response = requests.post(
        "http://127.0.0.1:8000/code-fix",
        json={
            "prompt": f"""### Instruction: F
### Input:
{oracle_input.input_code}
### Response:
""",
            "temperature": 0,
            "max_new_tokens": 32,
        },
    )
    response.raise_for_status()
    return response.json()["response"]


from langchain_app.models.vicuna_request_llm import VicunaLLM
from langchain.memory import ConversationBufferMemory

from langchain_app.prompts.self_healing_code_prompt import template_suffix

memory = ConversationBufferMemory(memory_key="chat_history")
python_tool = PythonAstREPLTool()
multi_line = MultiLineHumanInputRun()
llm = VicunaLLM()

tools = [
    Tool(
        name="Python REPL",
        func=python_tool,
        description="useful for when you need to execute Python code",
    ),
    Tool(
        name="Calculator",
        func=call_code_endpoint,
        description="useful for when you need to answer questions about math",
        args_schema=CodeOracleInput,
    ),
]

prefix = template_suffix
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)
print("Using prompt: ", prompt.template)

llm_chain = LLMChain(llm=llm, prompt=prompt)
tool_names = [tool.name for tool in tools]
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)

agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)
agent_chain.run(
    input="Think of cat jokes and save them to a csv file called 'catjokes.csv'. INDENT the code appropriately."
)
