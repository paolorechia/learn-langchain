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
tools = load_tools(["python_repl", "multi_line_human"], llm=llm)

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
    """
Oh, wait, before your start your next question, we should go over one more tool that is available. 
The action MultiLineHuman can be used to ask help to a human.

Action: MultiLineHuman
Action Input: "Human, please fix this error for me?"

Observation: 
# Gladly so, you declared a variable with \_, which is an illegal character.
# Here's the right version:
empty_list = []


Thought: The Human helped me, I should use his observation as input to the shell
Action: Python REPL
Action Input: 
empty_list = []

Observation:
Thought: It worked this time. I have concluded the task.
Final Answer: The following script worked:
empty_list = []


OK, now you begin
Question: Ask from the help of a human about a topic.
You should then help him.

"""
)
