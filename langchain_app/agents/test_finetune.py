from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.utilities import SerpAPIWrapper

from langchain_app.models.vicuna_request_llm import VicunaLLM

# First, let's load the language model we're going to use to control the agent.
llm = VicunaLLM()

params = {
    "engine": "google",
    "gl": "us",
    "hl": "en",
}
search = SerpAPIWrapper(params=params)
# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["python_repl"], llm=llm)

tools.append(
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to ask with search",
    )
)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Now let's test it out!
agent.run(
    """Think of cat jokes and save them to a csv file called 'catjokes.csv'. INDENT the code appropriately."""
)
