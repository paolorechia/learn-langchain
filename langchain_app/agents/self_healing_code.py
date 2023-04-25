from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_app.prompts.self_healing_code_prompt import template

# from alpaca_request_llm import AlpacaLLM
from langchain_app.models.vicuna_request_llm import VicunaLLM

# First, let's load the language model we're going to use to control the agent.
llm = VicunaLLM()

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["python_repl"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Now let's test it out!
prompt = template.format("""Create cat jokes and print them.""")
agent.run(prompt)
