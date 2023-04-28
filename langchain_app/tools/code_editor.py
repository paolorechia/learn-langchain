from langchain.agents import Tool
from pydantic import BaseModel, Field
import tempfile
import subprocess

from typing import List

class CodeEditorAddCodeInput(BaseModel):
    input_code: str = Field()

class CodeEditorChangeCodeLineInput(BaseModel):
    input_code: str = Field()
    line: int = Field()

class CodeEditorDeleteCodeLinesInput(BaseModel):
    lines: List[int] = Field()


class CodeEditorTooling:
    def __init__(self) -> None:
        self.source_code: List[str] = []

    def add_code(self, add_code_input: CodeEditorAddCodeInput):
        new_lines_of_code =  [line for line in add_code_input.input_code.split("\n") if line]
        self.source_code.extend(new_lines_of_code)

    def change_code_line(self, change_code_line_input: CodeEditorChangeCodeLineInput):
        self.source_code[change_code_line_input.line -1] = change_code_line_input.input_code

    def delete_code_lines(self, delete_code_lines_input: CodeEditorDeleteCodeLinesInput):
        lines_to_delete = delete_code_lines_input.lines
        lines_to_delete.sort()
        lines_to_delete.reverse()

        for line in lines_to_delete:
            idx = line -1
            self.source_code.pop(idx) 

    def run_code(self):
        with tempfile.NamedTemporaryFile(buffering=0) as fp:
            lines_to_save = [line.encode("utf-8") for line in self.source_code]
            fp.writelines(lines_to_save)
            print("Source saved to file: ", fp.name)    

            completed_process = subprocess.run(["python3", fp.name], capture_output=True, timeout=10)

            print(completed_process, completed_process.stderr)
            succeeded = "Succeeded" if completed_process.returncode == 0 else "Failed"
            stdout = completed_process.stdout
            stderr = completed_process.stderr
            return f"Program {succeeded}\nStdout:{stdout}\nStderr:{stderr}"
        
    def display_code(self):
        code_string = ""
        for idx, line in enumerate(self.source_code):
            code_string += f"{idx + 1}: {line}\n"
        return code_string

    def build_add_code_tool(self):
        return Tool(
            name="CodeEditorAddCode",
            func=self.add_code,
            description="useful for when you need to execute Python code",
        )

    def build_change_code_line_tool(self):
        return Tool(
            name="CodeEditorChangeCodeLine",
            func=self.change_code_line,
            description="useful for when you need to execute Python code",
        )
    
    def build_delete_code_lines_tool(self):
        return Tool(
            name="CodeEditorDeleteLine",
            func=self.delete_code_lines,
            description="useful for when you need to execute Python code",
        )

    def build_run_tool(self):
        return Tool(
            name="CodeEditorRunCode",
            func=self.run_code,
            description="useful for when you need to execute Python code",
        )