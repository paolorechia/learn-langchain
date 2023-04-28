from transformers import AutoTokenizer
import os
from gptq_for_llama.llama_inference import load_quant


def load_4_bit(config):
    model_path = config.model_path
    model_checkpoint = config.model_checkpoint
    if not model_path:
        if config.base_model_size == "13b":
            model_path = "vicuna-13B-1.1-GPTQ-4bit-128g"

            if not model_checkpoint:
                model_checkpoint = "vicuna-13B-1.1-GPTQ-4bit-128g.safetensors"

        else:
            model_path = "vicuna-7B-1.1-GPTQ-4bit-128g"

            if not model_checkpoint:
                model_checkpoint = "vicuna-7B-1.1-GPTQ-4bit-128g.safetensors"

    if not os.path.exists(model_path):
        if config.base_model_size == "7b":
            raise ValueError(
                """
Please clone the 7B model from HF and install the 'gpqt_for_llama' dependencies. To clone, run:

git clone https://huggingface.co/TheBloke/vicuna-7B-1.1-GPTQ-4bit-128g
"""
            )

        raise ValueError(
            """
Please clone the 13B model from HF and install the 'gpqt_for_llama' dependencies. To clone, run:
        
git clone https://huggingface.co/TheBloke/vicuna-13B-1.1-GPTQ-4bit-128g
"""
        )

    checkpoint = os.path.join(model_path, model_checkpoint)
    print("Loading model", model_path, " checkpoint", checkpoint)
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = load_quant(model_path, checkpoint, 4, 128)
    model.to(config.device)
    return model, tokenizer
