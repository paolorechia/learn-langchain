from alpaca_llm import AlpacaLLM
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class PromptRequest(BaseModel):
    prompt: str

alpaca = AlpacaLLM(max_tokens=512)
@app.post("/prompt")
def read_root(prompt_request: PromptRequest):
    print("Received prompt: ", prompt_request.prompt)
    return {"response": alpaca._call(prompt_request.prompt)}