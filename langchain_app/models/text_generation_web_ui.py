from langchain_app.models.http_llm import HTTPBaseLLM

STOP_TOKEN = "Observation"
def default_parameters():
    return {
        "max_new_tokens": 250,
        "do_sample": True,
        "temperature": 0.001,
        "top_p": 0.1,
        "typical_p": 1,
        "repetition_penalty": 1.2,
        "top_k": 1,
        "min_length": 32,
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
        "stopping_strings": [STOP_TOKEN + ":"],
    }


def response_extractor(json_response):
    result = json_response["results"][0]["text"]
    if STOP_TOKEN in result:
        return result.split(STOP_TOKEN)[0]
    return result


def build_text_generation_web_ui_client_llm(
    prompt_url="http://localhost:5000/api/v1/generate", parameters=None
):
    if parameters is None:
        parameters = default_parameters()

    return HTTPBaseLLM(
        prompt_url=prompt_url,
        parameters=parameters,
        stop_parameter_name="stopping_strings",
        response_extractor=response_extractor,
    )
