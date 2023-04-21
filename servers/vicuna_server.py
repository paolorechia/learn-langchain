"""Inference for Vicuna models."""
import torch
from typing import Optional, List
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaTokenizer, LlamaForCausalLM, AutoModel, LlamaForCausalLM
except ImportError:
    from transformers import AutoTokenizer, AutoModelForCausalLM, LLaMATokenizer, LLamaForCausalLM, AutoModel
from peft import PeftModel

def load_model(model_path, device="cuda", debug=False, use_fine_tuned_lora=True, lora_weights=""):
    if device == "cpu":
        kwargs = {}
    elif device == "cuda":
        kwargs = {"torch_dtype": torch.float16}
        kwargs["device_map"] = "auto"

    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)


    model = AutoModelForCausalLM.from_pretrained(model_path,
        low_cpu_mem_usage=True, load_in_8bit=True, **kwargs)

    if use_fine_tuned_lora:
        if not lora_weights:
            raise ValueError("Provide path to lora weights or set 'use_fine_tuned_lora' to False")
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            torch_dtype=torch.float16,
        )
    if device == "cuda":
        model.to(device)

    if debug:
        print(model)

    return model, tokenizer

device = "cuda"
model, tokenizer = load_model("../learn-vicuna/vicuna-7b/", device, lora_weights="../vicuna-react-lora/vicuna-react")

@torch.inference_mode()
def compute_until_stop(model, tokenizer, params, device,
                    context_len=2048, stream_interval=2):
    prompt = params["prompt"]
    temperature = float(params.get("temperature", 1.0))
    max_new_tokens = int(params.get("max_new_tokens", 256))
    stop_parameter = params.get("stop", None)
    if stop_parameter == tokenizer.eos_token:
        stop_parameter = None
    stop_strings = []
    if isinstance(stop_parameter, str):
        stop_strings.append(stop_parameter)
    elif isinstance(stop_parameter, list):
        stop_strings = stop_parameter
    elif stop_parameter is None:
        pass
    else:
        raise TypeError("Stop parameter must be string or list of strings.")

    input_ids = tokenizer(prompt).input_ids
    output_ids = []

    max_src_len = context_len - max_new_tokens - 8
    input_ids = input_ids[-max_src_len:]
    stop_word = None

    for i in range(max_new_tokens):
        if i == 0:
            out = model(
                torch.as_tensor([input_ids], device=device), use_cache=True)
            logits = out.logits
            past_key_values = out.past_key_values
        else:
            out = model(input_ids=torch.as_tensor([[token]], device=device),
                        use_cache=True,
                        past_key_values=past_key_values)
            logits = out.logits
            past_key_values = out.past_key_values

        last_token_logits = logits[0][-1]


        if temperature < 1e-4:
            token = int(torch.argmax(last_token_logits))
        else:
            probs = torch.softmax(last_token_logits / temperature, dim=-1)
            token = int(torch.multinomial(probs, num_samples=1))

        output_ids.append(token)

        if token == tokenizer.eos_token_id:
            stopped = True
        else:
            stopped = False


        output = tokenizer.decode(output_ids, skip_special_tokens=True)
        # print("Partial output:", output)
        for stop_str in stop_strings:
            # print(f"Looking for '{stop_str}' in '{output[:l_prompt]}'#END")
            pos = output.rfind(stop_str)
            if pos != -1:
                # print("Found stop str: ", output)
                output = output[:pos]
                # print("Trimmed output: ", output)
                stopped = True
                stop_word = stop_str
                break
            else:
                pass
                # print("Not found")

        if stopped:
            break

    del past_key_values
    if pos != -1:
        return output[:pos]
    return output


from fastapi import FastAPI
from pydantic import BaseModel
from pprint import pprint

app = FastAPI()
class PromptRequest(BaseModel):
    prompt: str
    temperature: float
    max_new_tokens: int
    stop: Optional[List[str]] = None

@app.post("/prompt")
def process_prompt(prompt_request: PromptRequest):
    params = {
        "prompt": prompt_request.prompt,
        "temperature": prompt_request.temperature,
        "max_new_tokens": prompt_request.max_new_tokens,
        "stop": prompt_request.stop
    }
    print("Received prompt: ", params["prompt"])
    # request with params...")
    # pprint(params)
    output = compute_until_stop(model, tokenizer, params, device)
    print("Output: ", output)
    return {"response": output}