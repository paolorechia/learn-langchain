from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
from transformers import LlamaForCausalLM, LlamaTokenizer

from langchain_app.utils.deprecation_warning import emit_module_deprecation_warning

emit_module_deprecation_warning(__name__)

model_path = "../alpaca-lora/llama-7b-hf"
model = LlamaForCausalLM.from_pretrained(
    model_path,
    load_in_8bit=True,
    device_map="auto",
)
tokenizer = LlamaTokenizer.from_pretrained(model_path, add_eos_token=True)


class LLama7BLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        input_text = prompt
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")

        outputs = model.generate(input_ids, max_length=512, temperature=0)
        return tokenizer.decode(outputs[0])

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
