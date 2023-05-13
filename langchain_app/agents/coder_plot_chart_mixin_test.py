from langchain.agents import (
    AgentExecutor,
    LLMSingleActionAgent,
    Tool,
    AgentOutputParser,
)
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from langchain_app.models.vicuna_request_llm import VicunaLLM
from langchain.schema import AgentAction, AgentFinish

from code_it.langchain.python_langchain_tool_mixin import LangchainPythonToolMixin

import re
from typing import List, Union


llm = VicunaLLM()

code_editor = LangchainPythonToolMixin()

tools = [
    code_editor.build_add_code_tool(),
    code_editor.build_run_tool(),
    code_editor.build_pip_install()
]

template = """You're a programmer AI.

You are asked to code a certain task.
You have access to a Code Editor, that can be used through the following tools:

{tools}


You should ALWAYS think what to do next.

Use the following format:

Task: the input task you must implement
Current Source Code: Your current code state that you are editing
Thought: you should always think about what to code next
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: The result of your last action
... (this Thought/Action/Action Input/Source Code/Code Result can repeat N times)

Thought: I have finished the task
Task Completed: the task has been implemented

Example task:
Task: the input task you must implement

Thought: To start, we need to add the line of code to print 'hello world'
Action: CodeEditorAddCode
Action Input: 
print("hello world") end of llm ouput
Observation:None

Thought: I have added the line of code to print 'hello world'. I should execute the code to test the output
Action: CodeEditorRunCode
Action Input: 

Observation:Program Succeeded
Stdout:b'hello world\n'
Stderr:b''

Thought: The output is correct, it should be 'hello world'
Action: None
Action Input:
Output is correct

Observation:None is not a valid tool, try another one.

Thought: I have concluded that the output is correct
Task Completed: the task is completed.


REMEMBER: don't install the same package more than once

Now we begin with a real task!

Task: {input}
Source Code: {source_code}

{agent_scratchpad}

Thought:"""


# Set up a prompt template
class CodeEditorPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    code_editor: LangchainPythonToolMixin
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
        kwargs["source_code"] = code_editor.display_code()
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)


prompt = CodeEditorPromptTemplate(
    template=template,
    code_editor=code_editor,
    tools=tools,
    input_variables=["input", "intermediate_steps"],
)


class CodeEditorOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        print("llm output: ", llm_output, "end of llm ouput")
        # Check if agent should finish
        if "Task Completed:" in llm_output:
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


output_parser = CodeEditorOutputParser()

llm_chain = LLMChain(llm=llm, prompt=prompt)
llm = VicunaLLM()

tool_names = [tool.name for tool in tools]
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names,
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)

agent_executor.run(
    """
Your job is to plot an example chart using matplotlib. Create your own random data.
Run this code only when you're finished.
DO NOT add code and run into a single step.
"""
)
