from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
# from alpaca_request_llm import AlpacaLLM
from vicuna_request_llm import VicunaLLM

# First, let's load the language model we're going to use to control the agent.
llm = VicunaLLM()

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(['python_repl'], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Now let's test it out!
agent.run("""

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

Example 3:

Question: Write and execute a script that sleeps for 2 seconds and prints 'Hello, World'
Thought: I should import the sleep function.
Action: Python REPL
Action Input: 
from time import sleep
Observation: 

Thought: I should call the sleep function passing 2 as parameter
Action: Python REPL
Action Input: 
sleep(2)
Observation: 

Thought: I should use the 'print' function to print 'Hello, World'
Action: Python REPL
Action Input: 
print('Hello, World')
Observation: 

Thought: I now finished the script
Final Answer: I executed the following script successfully:

from time import sleep
sleep(2)
print('Hello, World')


Additional Hints:
1. If an error thrown along the way, try to understand what happened and retry with a new code version that fixes the error.
2. DO NOT IGNORE ERRORS.
3. If an object does not have an attribute, call dir(object) to debug it.
4. SUPER IMPORTANT: ALWAYS respect the indentation in Python. Loops demand an idendentation. For example:

for i in range(10):
    print(i)  # this line has four spaces at the beginning

Same for ifs:

if True:
    print("hello")  # this line has four spaces at the beginning

An error be thrown because of the indentation, something like...  "expected an indented block after 'for' statement on line..."

To fix, make sure to indent the lines!

5. Do not use \ in variable names, otherwise you'll see the syntax error "unexpected character after line continuation character..."
6. If the variable is not defined, use vars() to see the defined variables.
7. Do not repeat the same statement twice without a new reason.
8. NEVER print the HTML directly.

Now begin for real!

Question: The website https://api.chucknorris.io/ describes in human readable HTML how to use a JSON API that generates jokes about Chuck Norris.
Write a script to:
1. fetch this website's HTML
2. save the results in a variable called 'response'
3. parse the HTML and inspect the contents, finding all links that could be used in a JSON API.

Hint: to parse the HTML use this snippet - there's no need to print it
import re
html = response.text
links = re.findall("https://api.chucknorris.io/[a-z]+/[a-z]+", html)

4. Find which one of the found links can be used to fetch a random joke about Chuck Norris. Look for one that contains the word 'random'
6. Use this link, e.g., fetch it
7. extract the joke from the response. Here's an example response to help you extract the joke:
    {
        "icon_url" : "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
        "id" : "nvdxPp5BQK2iQWRbPxrHVg",
        "url" : "",
        "value" : "Chuck Norris died once. when greated by the grim reaper chuck proceded 2 round house kick the reaper.long story short death will never make that mistake again"
    } 
8. print the joke
9. inspect the joke result, and make a comment
10. finish

""")