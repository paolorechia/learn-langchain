from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

# from alpaca_request_llm import AlpacaLLM
from langchain_app.models.vicuna_request_llm import VicunaLLM
from langchain_app.models.llama_http_llm import build_llama_base_llm

# First, let's load the language model we're going to use to control the agent.
# llm = VicunaLLM()
llm = build_llama_base_llm()

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["python_repl"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Now let's test it out!
agent.run(
    """
For instance:

Question: Find out how much 2 plus 2 is.
Thought: I must use the Python shell to calculate 2 + 2
Action: Python REPL
Action Input: 
2 + 2
Observation: 4

Thought: I now know the answer
Final Answer: 4

Example 2:
Question: You have a variable age in your scope. If it's greater or equal than 21, say OK. Else, say Nay.
Thought: I should write an if/else block in the Python shell.
Action: Python REPL
Action Input:
if age >= 21:
    print("OK")  # this line has four spaces at the beginning
else:
    print("Nay")  # this line has four spaces at the beginning

Observation: OK
Thought: I now know the answer
Final Answer: I have executed the task successfully.

Now begin for real!

Question: Write a Python script that prints "Hello, world!"
"""
)
