"""This modules experiments building logic from scratch, without langchain."""
from langchain_app.models.text_generation_web_ui import build_text_generation_web_ui_client_llm
from langchain_app.tools.code_editor import CodeEditorTooling
from langchain_app.simple_loop.planner import Planner
from langchain_app.simple_loop.coder import Coder
from langchain_app.simple_loop.refactor import Refactor

ANSWER_PATTERN = r"[a-zA-Z]+"

planner_parameters = {
    "max_new_tokens": 250,
    "do_sample": True,
    "temperature": 0.001,
    "top_p": 0.1,
    "typical_p": 1,
    "repetition_penalty": 1.13,
    "top_k": 1,
    "min_length": 0,
    "no_repeat_ngram_size": 0,
    "num_beams": 1,
    "penalty_alpha": 0,
    "length_penalty": 1.5,
    "early_stopping": False,
    "seed": -1,
    "add_bos_token": True,
    "truncation_length": 2048,
    "ban_eos_token": False,
    "skip_special_tokens": True,
    "stopping_strings": ["Observation:"],
}

coder_parameters = {
        "max_new_tokens": 250,
        "do_sample": True,
        "temperature": 0.001,
        "top_p": 0.1,
        "typical_p": 1,
        "repetition_penalty": 1.18,
        "top_k": 40,
        "min_length": 0,
        "no_repeat_ngram_size": 0,
        "num_beams": 1,
        "penalty_alpha": 0,
        "length_penalty": 1.5,
        "early_stopping": False,
        "seed": -1,
        "add_bos_token": True,
        "truncation_length": 2048,
        "ban_eos_token": False,
        "skip_special_tokens": True,
        "stopping_strings": ["Observation:"],
}

code_editor = CodeEditorTooling()
planner_llm = build_text_generation_web_ui_client_llm(parameters=planner_parameters)
coder_llm = build_text_generation_web_ui_client_llm(parameters=coder_parameters)
refactoring_llm = build_text_generation_web_ui_client_llm(parameters=coder_parameters)

planner = Planner()
coder = Coder()
refactor = Refactor()

task = "Your job is to generate 10 cat jokes and save in a file called 'cat_jokes.txt'. Be creative!"

planner_prompt = planner.prompt_template.format(task=task)
plan = planner_llm._call(planner_prompt, stop=[planner.stop_string])
plan = planner.parse_output(plan)
print(type(plan))
print("Parsed plan", plan)

for step in plan:
    print("Coding step ", step)
    coder_prompt = coder.prompt_template.format(subtask=step, source_code=code_editor.display_code())
    coding_result = coder_llm._call(coder_prompt, stop=[coder.stop_string])
    new_code = coder.parse_output(coding_result)
    code_editor.add_code(new_code)
print("Finished generating code!")


print("Current code", code_editor.display_code())
refactored = refactoring_llm._call(refactor.prompt_template.format(source_code=code_editor.display_code(), task=task), stop=[coder.stop_string])
print("After refactoring")
code_editor.overwrite_code(refactored)
print(code_editor.display_code())