from langchain.agents import Tool
from pydantic import BaseModel, Field
import tempfile
import subprocess

from typing import List

class CodeEditorChangeCodeLineInput(BaseModel):
    input_code: str = Field()
    line: int = Field()

class CodeEditorDeleteCodeLinesInput(BaseModel):
    lines: List[int] = Field()


class CodeEditorTooling:
    def __init__(self) -> None:
        self.source_code: List[str] = []
        self.filename = "persistent_source.py"
        self.new_code_candidate = ""
    
    def push_new_code_candidate(self, new_code: str):
        self.new_code_candidate = new_code

    def add_code_to_top(self, add_code_input: str):
        new_lines_of_code =  [line for line in add_code_input.split("\n") if line]
        self.source_code = new_lines_of_code + self.source_code
        self.save_code()
        return self.display_code()

    def add_code(self, add_code_input: str):
        new_lines_of_code =  [line for line in add_code_input.split("\n") if line]
        self.source_code.extend(new_lines_of_code)
        self.save_code()
        return self.display_code() 

    def change_code_line(self, change_code_line_input: str):
        s = change_code_line_input.split("\n")
        line = int(s[0]) - 1
        code = s[1]
        self.source_code[line] = code
        self.save_code()
        return self.display_code() 

    def delete_code_lines(self, delete_code_lines_input: str):
        lines_to_delete = [int(x) for x in delete_code_lines_input.split(",")]
        lines_to_delete.sort()
        lines_to_delete.reverse()

        for line in lines_to_delete:
            idx = line -1
            self.source_code.pop(idx)
        self.save_code()
        return self.display_code() 


    def save_code(self, *args, **kwargs):
        with open(self.filename, "w") as fp:
        # with tempfile.NamedTemporaryFile(buffering=0) as fp:
            # lines_to_save = [line.encode("utf-8") for line in self.source_code]
            # fp.writelines(lines_to_save)
            # filename = fp.name

            fp.write("\n".join(self.source_code))

    def run_code(self, *args, **kwargs):
        completed_process = subprocess.run(["python3", self.filename], capture_output=True, timeout=10)

        print(completed_process, completed_process.stderr)
        succeeded = "Succeeded" if completed_process.returncode == 0 else "Failed"
        stdout = completed_process.stdout
        stderr = completed_process.stderr
        return f"Program {succeeded}\nStdout:{stdout}\nStderr:{stderr}"
        
    def display_code(self):
        code_string = "\n"
        for idx, line in enumerate(self.source_code):
            code_string += f"{line}\n"
        return code_string

    def build_add_code_tool(self):
        return Tool(
            name="CodeEditorAddCode",
            func=self.add_code,
            description="""Use to add new lines of code. Example:
Action: CodeEditorAddCode
Action Input:
print("foo bar")

Observation: print("foo bar")

    Example 2. One can also use it to add several lines of code simultaneously:

Action: CodeEditorAddCode
Action Input: 
x = 2 + 3

Observation: x = 2 + 3

""",
        )
    
    def build_add_code_to_top_tool(self):
        return Tool(
            name="CodeEditorAddCodeToTop",
            func=self.add_code_to_top,
            description="""Use to add new lines of code at the beginning of the file. Example:

Source Code:
def parse_json(j):
    return json.load(j)

Action: CodeEditorAddCodeToTop
Action Input:
import json

Observation: 
import json
def parse_json(j):
    return json.load(j)
""",)
    
    def build_change_code_line_tool(self):
        return Tool(
            name="CodeEditorChangeCodeLine",
            func=self.change_code_line,
            description="""Use to modify an existing line of code. First line of input is line number and second line is new line of code to insert.

            Example that modifies line 3:

Source Code:
def my_func(x, y):
    return x * y
my_func(2, 3)

Action: CodeEditorChangeCodeLine
Action Input:
3
print("Line 3 now prints this")

Observation:
my_func(x, y):
    return x * y
print("Line 3 now prints this")

""",
        )
    
    def build_delete_code_lines_tool(self):
        return Tool(
            name="CodeEditorDeleteLine",
            func=self.delete_code_lines,
            description="""Use to delete lines of code.
            
            Example, to delete lines 1 and 3 of the source code.

Source Code:
def my_func(x, y):
    return x * y
my_func(2, 3)

Action: CodeEditorDeleteLine
Action Input:
1, 3
Observation: 
return x * y

""",
        )

    def build_run_tool(self):
        return Tool(
            name="CodeEditorRunCode",
            func=self.run_code,
            description="""Use to execute the script. Should always be called like this:

Action: CodeEditorRunCode
Action Input:
Observation: 
Observation:Program Succeeded
Stdout:b'Hello, world!'
Stderr:b''

Thought: In this example, the output of the program was b'Hello, world!'
Task Completed: the task was successfully completed

Example 2 (failure example):
Action: CodeEditorRunCode
Action Input:
Observation: 
Observation:Program Failed
Stdout:b''
Stderr:b''^^^^^\nSyntaxError: invalid syntax\n'

Thought: In this example, the program failed due to SyntaxError




""",
        )

    def build_display_code_tool(self):
        return Tool(
            name="CodeEditorDisplayCode",
            func=self.display_code,
            description="""Use to display current source code. Example:
Action: CodeEditorDisplayCode
Action Input:

Observation:
print("foo bar")
""",
        )