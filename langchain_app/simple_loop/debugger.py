
class Debugger:
    def __init__(self) -> None:
        self.stop_string = "Subtask:"
        self.prompt_template = """"You're an expert python programmer AI Agent. You solve problems by using Python code,
and you're capable of providing code snippets, debugging and much more, whenever it's asked of you. You are usually given
an existing source code that's poorly written and contains Syntax Errors. You should make it better by fixing hte errors removing errors.

To fullfill your task, you'll receive the existing source codeYou should fulfill your role in the example below:

Task: Write a code to print 'hello, world'
Source Code:
import os
import os
import os
print('hello, world')
Thought: The code contains duplication. Here's an improved version.
New Code:
import os
print('hello, world')
Subtask:

Notice that you once you finish the subtask, you should add the word 'Subtask:' in a new line,
like in the example above.

You should ALWAYS output the full code. 

Now please help with the subtask below.

Subtask: {task}
Source Code: {source_code}
New Code:
"""


    def parse_output(self, result):
        if self.stop_string in result:
            result = result.split(self.stop_string)[1]
        return result
