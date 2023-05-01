"""This modules experiments building logic from scratch, without langchain."""
from langchain_app.models.text_generation_web_ui import build_text_generation_web_ui_client_llm
from langchain_app.tools.code_editor import CodeEditorTooling
from langchain_app.simple_loop.planner import Planner
from langchain_app.simple_loop.coder import Coder
from langchain_app.simple_loop.code_editor_agent import CodeEditorAgent

ANSWER_PATTERN = r"[a-zA-Z]+"

from time import sleep
code_editor = CodeEditorTooling()
llm = build_text_generation_web_ui_client_llm()
planner = Planner()
coder = Coder()
code_editor_agent = CodeEditorAgent(llm, code_editor)

task = "Your job is to generate 10 cat jokes and save in a file called 'cat_jokes.txt'. Be creative!"

planner_prompt = planner.prompt_template.format(task=task)
plan = llm._call(planner_prompt, stop=[planner.stop_string])
print("Raw plan", plan)
plan = planner.parse_output(plan)
print(type(plan))
print("Parsed plan", plan)

for step in plan:
    print("Coding step ", step)
    coder_prompt = coder.prompt_template.format(subtask=step, source_code=code_editor.display_code())
    coding_result = llm._call(coder_prompt, stop=[coder.stop_string])
    new_code = coder.parse_output(coding_result)
    print("Coding result", new_code)
    code_editor.push_new_code_candidate(new_code)
    try:
        code_editor_agent.execute(step)
    except ValueError as excp:
        print(excp)
        raise excp
    print("Finished code editor step")
    print("Sleeping...")
    sleep(5)

print("Finished!")