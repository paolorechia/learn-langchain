from transformers import AutoTokenizer
import os
from gptq_for_llama.llama_inference import load_quant


def load_4_bit(config):
    if config.base_model_size == "13b":
        raise NotImplementedError("13b not yet supported")

    if not model_path:
        model_path = "vicuna-AlekseyKorshuk-7B-GPTQ-4bit-128g"
    
    if not checkpoint_path:
        checkpoint_path = "vicuna-AlekseyKorshuk-7B-GPTQ-4bit-128g.safetensors"
    if not os.path.exists(model_path):
        raise ValueError(
            """
Please clone the 7B model from HF and install the 'gpqt_for_llama' dependencies. To clone, run:
            
git clone https://huggingface.co/TheBloke/vicuna-AlekseyKorshuk-7B-GPTQ-4bit-128g
"""
        )

    checkpoint = os.path.join(model_path, checkpoint_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = load_quant(model_path, checkpoint, 4, 128)
    model.to(config.device)
    return model, tokenizer