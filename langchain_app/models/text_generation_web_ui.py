from http_llm import HTTPBaseLLM
from langchain_app.models.http_llm import HTTPBaseLLM


def default_parameters():
    return {
        "max_new_tokens": 250,
        "do_sample": True,
        "temperature": 1.3,
        "top_p": 0.1,
        "typical_p": 1,
        "repetition_penalty": 1.18,
        "top_k": 40,
        "min_length": 0,
        "no_repeat_ngram_size": 0,
        "num_beams": 1,
        "penalty_alpha": 0,
        "length_penalty": 1,
        "early_stopping": False,
        "seed": -1,
        "add_bos_token": True,
        "truncation_length": 2048,
        "ban_eos_token": False,
        "skip_special_tokens": True,
        "stopping_strings": ["Observation:"],
    }


def build_text_generation_web_ui_client_llm(
    prompt_url="http://localhost:5000/api/v1/generate", parameters=None
):
    if parameters is None:
        parameters = default_parameters()

    return HTTPBaseLLM(prompt_url=prompt_url, parameters=parameters)
