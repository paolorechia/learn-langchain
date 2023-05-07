"""Inference for Vicuna models."""
from typing import Optional, List
from servers.load_config import Config
from servers.model_inference import get_embeddings, compute_until_stop
import os
import json

config = Config()

print("Using config: ", config)

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
    logging_session: Optional[str] = None


class EmbeddingRequest(BaseModel):
    prompt: str


class PromptLogger:
    _instances = {}

    @staticmethod
    def get(session):
        if session not in PromptLogger._instances:
            PromptLogger._instances[session] = PromptLogger(session)
        return PromptLogger._instances[session]

    def __init__(self, session) -> None:
        self.input_step = 0
        self.output_step = 0
        self.session = session
        self._dir = f"logged_prompts/session_{session}/"
        try:
            os.makedirs(self._dir)
        except FileExistsError:
            pass

    def log(self, input_str, prefix="input"):
        filename = os.path.join(self._dir, f"{prefix}_{self.input_step}")
        with open(filename, "w") as fp:
            if prefix == "input":
                input_str = input_str.split("Now begin for real!\n")[1]
            fp.write(input_str)

        if prefix == "input":
            self.input_step += 1
        elif prefix == "output":
            self.output_step += 1
        else:
            raise ValueError("Invalid prefix")



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
    if prompt_request.logging_session is not None:
        prompt_logger = PromptLogger.get(prompt_request.logging_session)
        prompt_logger.log(prompt_request.prompt, prefix="input")
        prompt_logger.log(output, prefix="output")

    return {"response": output}


@app.post("/embedding")
def embeddings(prompt_request: EmbeddingRequest):
    params = {"prompt": prompt_request.prompt}
    print("Received prompt: ", params["prompt"])
    output = get_embeddings(model, tokenizer, params["prompt"])
    return {"response": [float(x) for x in output]}
