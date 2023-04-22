from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

import torch
from peft import PeftModel
import transformers
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig


model_path = "../alpaca-lora/llama-7b-hf"
# model_path = "../alpaca-lora/llama-13b-hf"
# model_path = "decapoda-research/llama-30b-hf"
alpaca_path = "../alpaca-lora/alpaca-lora-7b"
# alpaca_path = "../alpaca-lora/alpaca-lora-13b"
# alpaca_path = "chansung/alpaca-lora-30b"
# alpaca_path = "lora-alpaca-stardew-valley"

tokenizer = LlamaTokenizer.from_pretrained(model_path)

model = LlamaForCausalLM.from_pretrained(
    model_path,
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)
model = PeftModel.from_pretrained(
    model,
    alpaca_path,
    torch_dtype=torch.float16,
    device_map={"": 0}
)

model.eval()


class AlpacaLLM(LLM):        
    temperature: float = 0.1
    top_p: float = 0.75
    top_k: int = 40j
    num_beams: int = 4
    max_tokens: int = 2048

    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].cuda()
        generation_config = GenerationConfig(
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            num_beams=self.num_beams
        )
        with torch.no_grad():
            generation_output = model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=self.max_tokens,
            )
        s = generation_output.sequences[0]
        output = tokenizer.decode(s)
        return output


    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "num_beams": self.num_beams,
        }
