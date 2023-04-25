"""Inference for Vicuna models."""
from typing import Optional, List
from servers.load_config import Config
from servers.model_inference import get_embeddings, compute_until_stop

config = Config()

print("Using config: ", config)

model_path = config.model_path
checkpoint_path = config.checkpoint_path

if config.use_4bit:
    from servers.quant_loader import load_4_bit

    model, tokenizer = load_4_bit(config)
else:
    from servers.hf_loader import load_16_bit

    model, tokenizer = load_16_bit(config)


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str
    temperature: float
    max_new_tokens: int
    stop: Optional[List[str]] = None


class EmbeddingRequest(BaseModel):
    prompt: str


@app.post("/prompt")
def process_prompt(prompt_request: PromptRequest):
    params = {
        "prompt": prompt_request.prompt,
        "temperature": prompt_request.temperature,
        "max_new_tokens": prompt_request.max_new_tokens,
        "stop": prompt_request.stop,
    }
    print("Received prompt: ", params["prompt"])
    output = compute_until_stop(model, tokenizer, params, config.device)
    print("Output: ", output)
    return {"response": output}


@app.post("/embedding")
def embeddings(prompt_request: EmbeddingRequest):
    params = {"prompt": prompt_request.prompt}
    print("Received prompt: ", params["prompt"])
    output = get_embeddings(model, tokenizer, params["prompt"])
    return {"response": [float(x) for x in output]}
