"""Inference for Starcode model loaded in 8bit."""
from transformers import AutoModelForCausalLM, AutoTokenizer
from servers.model_inference import compute_until_stop
from typing import Optional, List

checkpoint = "bigcode/starcoder"
device = "cuda" # for GPU usage or "cpu" for CPU usage

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint, trust_remote_code=True, load_in_8bit=True, device_map="auto")
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int
    stop: Optional[List[str]] = None


@app.post("/prompt")
def process_prompt(prompt_request: PromptRequest):
    print("Received prompt: ", prompt_request.prompt)
    print("Max new tokens: ", prompt_request.max_new_tokens)
    params = {
        "prompt": prompt_request.prompt,
        "max_new_tokens": prompt_request.max_new_tokens,
        "stop": prompt_request.stop,
    }
    result = compute_until_stop(model, tokenizer, params, device, context_len=8192)
    print("Result: ", result)
    return {"response": result}
