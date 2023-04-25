from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.utilities import SerpAPIWrapper
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()

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

Action: MultiLineHuman
Action Input: "Human, please fix this error for me?"

Observation: 
# Gladly so, you declared a variable with \_, which is an illegal character.
# Here's the right version:
empty_list = []


Thought: I need to call the Python REPL again using the human insight.
Action: Python REPL
Action Input: 
empty_list = []

Observation:
Thought: It worked this time. I have concluded the task.
Final Answer: The following script worked:
empty_list = []


(Some additional hints)
(hint: If you get stuck, ask for help from human, don't try to fix two errors in a sequence)
(hint2: When a human gives you some code, you should execute it using Python REPL, for example:

(...)

Thought:I should indent the block after the for statement
Action: Python REPL
Action Input: 
jokes = []
for i in range(5):
jokes.append(random.choice(["You can't have just one cat!", "Why did the cat cross the road?", "I'm not a cat person, but I love cats.", "I'm not a dog person, but I love dogs.", "I'm not a cat person, but I love cats. They're so independent."]))

Observation: expected an indented block after 'for' statement on line 2 (<string>, line 3)
Thought:I should ask for help from a human
Action: MultiLineHuman
Action Input: "Human, please help me with this error."

Observation: jokes = []
for i in range(5):
    jokes.append(random.choice(["You can't have just one cat!", "Why did the cat cross the road?", "I'm not a cat person, but I love cats.", "I'm not a dog person, but I love dogs.", "I'm not a cat person, but I love cats. They're so independent."]))

Thought: I should now execute the human's code snippet
Action: Python REPL    
Action Input: 
jokes = []
for i in range(5):
    jokes.append(random.choice(["You can't have just one cat!", "Why did the cat cross the road?", "I'm not a cat person, but I love cats.", "I'm not a dog person, but I love dogs.", "I'm not a cat person, but I love cats. They're so independent."]))

Observation:
Thought: It worked, I should now continue with the next step.
(... continue until Final answer)


(hint2.example3)

(...)

Thought:I should check the variable x
Action: Python REPL
Action Input:
if x > 3:
print("Greater than 3")

Observation: expected an indented block after 'if' statement on line 2 (<string>, line 3)
Thought:I should ask for help from a human
Action: MultiLineHuman
Action Input: "Human, please help me with this error."

Observation: if x > 3:
    print("Greater than 3")

Thought: I should execute the human's code
Action: Python REPL
Action Input:
if x > 3:
    print("Greater than 3")

OK, now you begin
Question: 

1. Create 5 random cat jokes. Each joke should be self-contained into a string.
2. Write the jokes to a file.
3. Output the file contents to double check it's not empty.
4. Ask the human if the results are good.
5. Finished!

"""
)
