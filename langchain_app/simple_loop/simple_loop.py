"""This modules experiments building logic from scratch, without langchain."""
from langchain_app.models.vicuna_request_llm import VicunaLLM
from langchain_app.tools.code_editor import CodeEditorTooling
import re
from time import sleep
from langchain_app.simple_loop.prompts import Templates, Identities

ANSWER_PATTERN = r"[a-zA-Z]+"

code_editor = CodeEditorTooling()
llm = VicunaLLM()


task = "Your job is to generate 10 cat jokes and save in a file called 'cat_jokes.txt'. Be creative!"

STOP_TOKEN = "###END_OF_GENERATION"
executed_actions = []
top_level_actions = ["AddCode", "RunCode", "AskHuman", "GiveUp"]
memory = {}
last_action_result = ""
last_action = ""

def strip_hallucination(output):
    if Identities.MASTERMIND in output:
        return output.split(Identities.MASTERMIND)[0]
    return output

def options_to_string(options):
    result = []
    for idx, option in enumerate(options):
        result.append(f"{idx + 1}. {option} {STOP_TOKEN}")

    return "\n".join(result)


while True:
    if executed_actions:
        last_action = executed_actions[-1]
    hint = ""
    if last_action:
        if last_action == "AddCode":
            hint = "HINT: try 2. RunCode"
    prompt = Templates.MASTERMIND_TEMPLATE.format(
        task=task,
        identity=Identities.GENERIC_AI,
        stop_token=STOP_TOKEN,
        options=options_to_string(top_level_actions),
        num_actions=len(executed_actions),
        memory=memory,
        last_action=last_action,
        last_action_result=last_action_result,
        hint=hint
    )

    print("First prompt ", prompt)
    result = llm._call(prompt, stop=[STOP_TOKEN])
    print("Raw result ", result)
    result = strip_hallucination(result)
    answer = result.split("AI Agent:")[-1]
    print(answer)

    findings = re.findall(ANSWER_PATTERN, answer)
    extracted_option = findings[0]

    print("Extracted option ", extracted_option)
            
    if extracted_option == "AddCode":
        # Let's prompt for what code
        prompt = Templates.ADD_CODE_TEMPLATE.format(
            identity=Identities.EXPERT_PROGRAMMER,
            task=task,
            num_actions=len(executed_actions),
            stop_token=STOP_TOKEN,
            memory=memory,
            last_action=last_action,
            last_action_result=last_action_result,
        )
        print("Second prompt ", prompt)
        output = llm._call(prompt, stop=[STOP_TOKEN])

        output = strip_hallucination(output)
        if "Programmer AI:" in output:
            output = output.split("Programmer AI:")[1]
        # print("Result")
        # print(output)
        code_editor.add_code(output)
        executed_actions.append(extracted_option)
        memory["source_code"] = code_editor.display_code()
        last_action_result = ""
    elif extracted_option == "RunCode":
        executed_actions.append(extracted_option)
        last_action_result = code_editor.run_code()
    else:
        raise NotImplementedError(f"{extracted_option} not yet implemented :(")

    print("Sleeping so Human understands WTH is going on")
    sleep(5)
