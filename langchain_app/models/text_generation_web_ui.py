from http_llm import HTTPBaseLLM


TextGenerationWebUILLM = HTTPBaseLLM(
    prompt_url="http://localhost/api/v1/generate",
    parameters={
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
    },
)
