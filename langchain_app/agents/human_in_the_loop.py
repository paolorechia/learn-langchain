from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.utilities import SerpAPIWrapper

from models.vicuna_request_llm import VicunaLLM

# First, let's load the language model we're going to use to control the agent.
llm = VicunaLLM()

params = {
    "engine": "google",
    "gl": "us",
    "hl": "en",
}
search = SerpAPIWrapper(params=params)
# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(['python_repl', 'human'], llm=llm)

tools.append(Tool(
    name="Search",
    func=search.run,
    description="useful for when you need to ask with search"
))

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Now let's test it out!
agent.run("""
Oh, wait, before your start your next question, we should go over one more tool that is available. 
The action Human can be used to ask help to a human.

For example:

Question: Create an empty list in Python
Thought: I should create an empty list in Python
Action: Python REPL
Action Input: 
empty_\list = []
Observation: unexpected character after line continuation character...

Thought: I have a syntax error and should fix it
Action: Python REPL
Action Input: 
empty_\list = []
Observation: unexpected character after line continuation character...
Thought: I could not understand how to fix this, I should ask for help from a Human.

Action: Human
Action Input: "Do you know the specific date of Eric Zhu's birthday?"

OK, now you begin
""")
