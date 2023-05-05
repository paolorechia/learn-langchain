from langchain_app.models.http_llm import HTTPBaseLLM


def default_parameters():
    return {"max_new_tokens": 512, "stop": ["-----"]}


def build_star_coder_llm(prompt_url="http://127.0.0.1:8000/prompt", parameters=None):
    if parameters is None:
        parameters = default_parameters()

    return HTTPBaseLLM(prompt_url=prompt_url, parameters=parameters)
