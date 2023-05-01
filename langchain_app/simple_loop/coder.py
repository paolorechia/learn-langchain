
class Coder:
    def __init__(self) -> None:
        self.stop_string = "Subtask:"
        self.prompt_template = """"You're an expert python programmer AI Agent. You solve problems by using Python code,
and you're capable of providing code snippets, debugging and much more, whenever it's asked of you. You are usually given
an existing source code and a small subtask. You should focus on fulfilling only the subtask by providing the required code. 

You should fulfill your role in the example below:

Source Code:
import os

Subtask: Write a code to print 'hello, world'
Programmer AI:
print('hello, world')
Subtask:

Notice that you once you finish the subtask, you should add the word 'Subtask:' in a new line,
like in the example above.

Now please help with the subtask below.

Source Code: {source_code}
Subtask: {subtask}
Programmer AI:
"""


    def parse_output(self, result):
        if self.stop_string in result:
            result = result.split(self.stop_string)[1]
        return result
