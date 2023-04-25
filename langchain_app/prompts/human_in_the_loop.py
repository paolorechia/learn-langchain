template_suffix = """A human is asking you to execute tasks, try your best to fulfill them. We'll go over several examples before trying the real task.

Example 1:
Question: Find out how much 2 plus 2 is.
Thought: I must use the Python shell to calculate 2 + 2
Action: Python REPL
Action Input: 
2 + 2  # line 1
Observation: 4

Thought: I now know the answer
Final Answer: 4


Example 2:
Question: Write and execute a script that sleeps for 2 seconds and prints 'Hello, World'
Thought: I should import the sleep function.
Action: Python REPL
Action Input: 
from time import sleep  # line 1
Observation: 

Thought: I should call the sleep function passing 2 as parameter
Action: Python REPL
Action Input: 
sleep(2)   # line 1
Observation: 

Thought: I should use the 'print' function to print 'Hello, World'
Action: Python REPL
Action Input: 
print('Hello, World')  # line 1
Observation: 

Thought: I now finished the script
Final Answer: I executed the following script successfully:

from time import sleep  # line 1
sleep(2)  # line 2
print('Hello, World')  # line 3


Example 3:
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

Example 4:
Question: Open a file and write 'Foo bar' to it.
Thought: I should create a Python code that opens a file and write 'Foo bar' it using the Python REPL
Action: Python REPL
Action Input:
with open("some_example_file.txt", "w") as fp: # line 1
    fp.write("Foo bar") # line 2 this has four spaces at the beginning, it's indented because of the with


Observation:

Thought: I now know the answer.
Final Answer: I have executed the task successfully.


Example 5:
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


Example 6 (this one demonstrates how to ask help from a human)

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


Additional Hints:
1. If an error thrown along the way, try to understand what happened and retry with a new code version that fixes the error.
2. DO NOT IGNORE ERRORS.
3. If an object does not have an attribute, call dir(object) to debug it.

An error be thrown because of the indentation, something like...  "expected an indented block after 'for' statement on line..."

To fix, make sure to indent the lines!

4. Do not use \ in variable names, otherwise you'll see the syntax error "unexpected character after line continuation character..."
5. If the variable is not defined, use vars() to see the defined variables.
6. Do not repeat the same statement twice without a new reason
7. NEVER use the function input() in Python
8. If you get stuck, ask for help from human, don't try to fix the same error twice.
9. When a human gives you some code, you should execute it using Python REPL.


You have access to the following tools:
"""
