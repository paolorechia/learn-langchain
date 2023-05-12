from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools.python.tool import PythonAstREPLTool
from langchain_app.models.llama_http_llm import build_llama_base_llm
import json


prompt_template = """

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
Thought: I have executed the task successfully.
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

Question: {}
"""

offset = 376
with open("task_generation/dedup_generated_tasks.json", "r") as fp:
    tasks = json.load(fp)
    tasks = tasks[offset:]


for idx, task in enumerate(tasks):
    params = {"temperature": 0, "max_new_tokens": 2048, "stop": ["Observation:"], "logging_session": f"medium_size_dataset{idx+offset}"}

    llm = build_llama_base_llm(parameters=params)
    python_tool = PythonAstREPLTool()

    tools = [
        Tool(
            name="Python REPL",
            func=python_tool,
            description="useful for when you need to execute Python code",
        ),
    ]
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    first_task = tasks[idx]
    try:
        agent.run(prompt_template.format(first_task))
    except Exception:
        pass