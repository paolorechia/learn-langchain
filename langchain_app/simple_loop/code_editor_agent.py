
from langchain.agents import (
    AgentExecutor,
    LLMSingleActionAgent,
    Tool,
    AgentOutputParser,
)
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from langchain_app.tools.code_editor import CodeEditorTooling
from langchain.schema import AgentAction, AgentFinish

import re
from typing import List, Union

template = """"You're an expert python programmer AI Agent, that works alongside another programmer.
You and the other programmer solves subtasks by implementing them in Python code.
You solve problems by receiving code snippets and modifying existing source code.
You have access to a code editor through the following tools:

{tools}

Your tasks will initially typically come in the following format:

Existing Source Code:
Subtask:
New Code From The Pair Programmer:

For example:

Existing Source Code:
def main():

Subtask: Write a function that calculates the sum of two numbers.
New Code From The Pair Programmer:
def sum_numbers(a: int, b: int) -> int:
    return a + b

To solve this, you need to use your tools to modify the existing source accordingly.
In the above example, using CodeEditorAddCodeToTop like this:

Thought: I must add the code from the pair programmer into the top
Action: CodeEditorAddCodeToTop
Action Input:
def sum_numbers(a: int, b: int) -> int:
    return a + b
Observation:
def sum_numbers(a: int, b: int) -> int:
    return a + b
def main():


Thought: I have successfully edited the code
Final Answer: I have finished my task

Example 2:

Existing Source Code:
def sum_numbers(a: int, b: int) -> int:
    return a + b
def main():

Subtask: Print the result of 3 + 7.
New Code From The Pair Programmer:
def sum_numbers(a: int, b: int) -> int:
    return a + b
def main():
    print(sum_numbers(3, 7)

Thought: I must merge the two code blocks, by only adding a new line at the bottom to print the sum
Action: CodeEditorAddCode
Action Input:
    print(sum_numbers(3, 7))
Observation: 
def sum_numbers(a: int, b: int) -> int:
    return a + b
def main():
    print(sum_numbers(3, 7)

Thought: I have successfully edited the code
Final Answer: I have finished my task



Example 3:

Existing Source Code:
def create_agent():
    return "stub"

Subtask: Create an agent inside the 'create_agent' function.
New Code From The Pair Programmer:
def create_agent():
    return Agent()

Thought: I must merge the two code blocks. I need to first delete the repeated code.
Action: CodeEditorDeleteLines
Action Input:
2

Observation: 
def create_agent():

Thought: I must merge the two code blocks. I can now add the new different line.
Action: CodeEditorAddCode
Action Input:
    return Agent()

Observation:
def create_agent():
    return Agent()

Thought: I have successfully edited the code
Final Answer: I have finished my task


Now try to solve the following.
Once you've seen that you have successfully edited the code, you should add a Thought followed by a Final Answer block.
You should ALWAYS think what to do next.

Existing Source Code: {source_code}
Subtask: {input}
New Code From The Pair Programmer: {new_code}
Agent scratchpad: {agent_scratchpad}
"""

# Set up a prompt template
class CodeEditorPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    code_editor: CodeEditorTooling
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        kwargs["source_code"] = self.code_editor.display_code()
        kwargs["new_code"] = self.code_editor.new_code_candidate
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)



class CodeEditorOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )




class CodeEditorAgent:
    def __init__(self, llm, code_editor:CodeEditorTooling) -> None:
        self.llm = llm
        code_editor = code_editor

        tools = [
            code_editor.build_add_code_tool(),
            code_editor.build_add_code_to_top_tool(),
            code_editor.build_change_code_line_tool(),
            code_editor.build_delete_code_lines_tool(),
            code_editor.build_run_tool(),
        ]

        prompt = CodeEditorPromptTemplate(
            template=template,
            code_editor=code_editor,
            tools=tools,
            input_variables=["input", "intermediate_steps"],
        )

        output_parser = CodeEditorOutputParser()

        llm_chain = LLMChain(llm=llm, prompt=prompt)

        tool_names = [tool.name for tool in tools]
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["Observation"],
            allowed_tools=tool_names,
        )

        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True
        )

    def execute(self, subtask):
        self.agent_executor.run(subtask)
