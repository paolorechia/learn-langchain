from langchain.agents import Tool
from pydantic import BaseModel, Field

from typing import List

class CodeEditorAddCodeInput(BaseModel):
    input_code: str = Field()

class CodeEditorChangeCodeLineInput(BaseModel):
    input_code: str = Field()
    line: int = Field()

class CodeEditorDeleteCodeLinesInput(BaseModel):
    input_code: str = Field()
    line: List[int] = Field()


class CodeEditorTooling:
    def __init__(self) -> None:
        self.source_code: List[str] = []

    def add_code(add_code_input: CodeEditorAddCodeInput):
        pass

    def change_code_line(change_code_line_input: CodeEditorChangeCodeLineInput):
        pass

    def delete_code_lines(delete_code_lines_inpuot: CodeEditorDeleteCodeLinesInput):
        pass

    def run_code(self):
        pass

    def build_add_code_tool(self):
        return Tool(
            name="CodeEditorAddCode",
            func=self.add_code,
            description="useful for when you need to execute Python code",
        )

    def build_change_code_line_toold(self):
        return Tool(
            name="CodeEditorChangeCodeLine",
            func=self.change_code_line,
            description="useful for when you need to execute Python code",
        )
    
    def build_delete_code_lines_tool(self):
        return Tool(
            name="CodeEditorDeleteLine",
            func=self.add_code,
            description="useful for when you need to execute Python code",
        )

    def build_run_tool(self):
        return Tool(
            name="CodeEditorRunCode",
            func=self.add_code,
            description="useful for when you need to execute Python code",
        )