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
    """

For instance:

Question: Find out how much 2 plus 2 is.
Thought: I must use the Python shell to calculate 2 + 2
Action: Python REPL
Action Input: 
2 + 2  # line 1
Observation: 4

Thought: I now know the answer
Final Answer: 4


Example 2:

Question: Find the complex solutions of the equation 5x^2 - 3x + 5 = 0
Thought: I must use the Wolfram API to find the complex solutions of the equation 5x^2 - 3x + 5 = 0
Action: Wolfram Alpha
Action Input: 
5x^2 - 3x + 5 = 0
Observation: Solution 1: x = 3/10 - (i sqrt(91))/10
Solution 2: x = 3/10 - (i sqrt(91))/10

Thought: I now know the answer
Final Answer: Solutions are x_{1,2} = 3/10 ± (i sqrt(91))/10

Example 3:

Question: Find a funny dog joke on Google
Thought: I must use the Google Serper to find dog jokes
Action: Search
Action Input:
dog jokes
Observation: What kind of dog is always up for taking a bath? A shampoo-dle.
Which kind of dog lives in Dracula’s castle? A bloodhound.


Thought: I should pick the best joke
Final Answer: What did the cowboy say when his dog ran away? “Well, doggone!”
Do you want to hear more jokes?


Example 4:
Question: You have a variable age in your scope. If it's greater or equal than 21, say OK. Else, say Nay.
Thought: I should write an if/else block in the Python shell.
Action: Python REPL
Action Input:
if age >= 21:  # line 1
    # line 2 - this line has four spaces at the beginning, it's indented because of the if
    print("OK")  # line 3 - this line has four spaces at the beginning, it's indented because of the if
else:  # line 4
    # line 5 - this line has four spaces at the beginning, it's indented because of the else
    print("Nay") # line 6  - this line has four spaces at the beginning, it's indented because of the else

Observation: OK

Thought: I now know the answer
Final Answer: I have executed the task successfully.

Example 5:
Question: Open a file and write 'Foo bar' to it.
Thought: I should create a Python code that opens a file and write 'Foo bar' it using the Python REPL
Action: Python REPL
Action Input:
with open("some_example_file.txt", "w") as fp: # line 1
    fp.write("Foo bar") # line 2 this has four spaces at the beginning, it's indented because of the with


Observation:

Thought: I now know the answer.
Final Answer: I have executed the task successfully.


Example 6:
Question: Open a HTTP connection using the requests.Session to the website https://somesite.com, and print the response status code.
Thought: I should use Python REPL to create the HTTP connection and print the response status code  
Action: Python REPL
Action Input:
import requests # line 1
with open(requests.Session() as session: # line 2
resp = session.get("https://sometime.com") # line 3
print(resp.status_code) # line 4

Observation: expected an indented block after 'with' statement on line 1 (<string>, line 3)

Thought: The lines after the 'with' statement have missing leading spaces. I should fix it.

Action: Python REPL
Action Input:
import requests # line 1
with open(requests.Session() as session: # line 2
    resp = session.get("https://sometime.com") # line 3 - this has four spaces at the beginning, it's indented because of the with
    print(resp.status_code) # line 4 - this has four spaces at the beginning, it's indented because of the with


Observation: 200

Thought: I now know the answer.
Final Answer: I have executed the task successfully.

Additional Hints:
1. If an error thrown along the way, try to understand what happened and retry with a new code version that fixes the error.
2. DO NOT IGNORE ERRORS.
3. If an object does not have an attribute, call dir(object) to debug it.

An error be thrown because of the indentation, something like...  "expected an indented block after 'for' statement on line..."

To fix, make sure to indent the lines!

5. Do not use \ in variable names, otherwise you'll see the syntax error "unexpected character after line continuation character..."
6. If the variable is not defined, use vars() to see the defined variables.
7. Do not repeat the same statement twice without a new reason
8. The ONLY tools available to use are: ['Python REPL', 'Wolfram Alpha', 'Search']


Now begin for real!

Question: Think of cat jokes and save them to a csv file called 'catjokes.csv'. INDENT the code appropriately.
"""
)
