class Identities:
    MASTERMIND = "Mastermind"
    GENERIC_AI = "You're an Agent AI"
    EXPERT_PROGRAMMER = """You're an expert python programmer AI Agent. You solve problems by using Python code,
    and you're capable of providing code snippets, debugging and much more, whenever it's asked of you.
    """
    HUMAN = "Human"

class Templates:
    MASTERMIND_TEMPLATE = """
    Mastermind: {identity} fulfilling the task: '{task}'
    Mastermind: So far you have performed {num_actions} actions towards your objective.
    Mastermind: You have this information in memory: {memory}
    Mastermind: Your previous action is {last_action}
    Mastermind: The result of your previous action is {last_action_result}

    Mastermind: You should decide on what to do. Carefully on the current state and what needs to be done next.
    Your options, pick one:

{options}

Please reply with the option number and add a {stop_token} after it.

For example:

1. AddCode {stop_token}

In this case you'll add more code to your memory / file to execute.

Example 2:

2. RunCode {stop_token}


In this case, you'll run the stored code and have access to the results.


Now your turn:

    {hint}
    AI Agent:"""



    ADD_CODE_TEMPLATE = """

    Mastermind: {identity} fulfilling the task: '{task}'
    Mastermind: So far you have performed {num_actions} actions towards your objective.
    Mastermind: You have this information in memory: {memory}
    Mastermind: Your previous action is {last_action}
    Mastermind: The result of your previous action is {last_action_result}
    Mastermind: You've chosen now to execute the action 'AddCode'
    Mastermind: Please provide the code you want to store in memory.

You should provide them as in the example(s):

For example, you could add the following code:

Programmer AI:
print('hello, world')
{stop_token}


Now try to fulfill the task '{task}'. Don't forget the {stop_token} at the end.

Programmer AI:"""