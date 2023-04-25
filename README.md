# learn-langchain

AI Agent with Vicuna

## Update 25.04
This repository has again been reorganized, adding support for 4 bit models (from gpqt_for_llama: https://github.com/qwopqwop200/GPTQ-for-LLaMa)

You can now change the server behavior by setting environment variables:

```python
class Config:
    def __init__(self) -> None:
        self.base_model_size = "13b" if os.getenv("USE_13B_MODEL") else "7b"
        self.use_for_4bit = True if os.getenv("USE_FOR_4BIT") else False
        self.use_fine_tuned_lora = True if os.getenv("USE_FINE_TUNED_LORA") else False
        self.lora_weights = os.getenv("LORA_WEIGHTS")
        self.device = "cpu" if os.getenv("USE_CPU") else "cuda"
        self.model_path = os.getenv("MODEL_PATH", "")
        self.checkpoint_path = os.getenv("MODEL_CHECKPOINT", "")
```

Some options are incompatible with each other, the code does not check for all possibilities.

This repository support the following models:

- Vicuna 7b unquantized, HF format (16-bits) - this is the default (https://huggingface.co/eachadea/vicuna-7b-1.1)
- Vicuna 7b LoRA fine-tune (8-bits)
- Vicuna 7b GPQT 4-bit group-size 128
- Vicuna 13b unquantized, HF format (16-bits)
- Vicuna 13b GPQT 4-bit group-size 128


## Update 21.04
This repository has been reorganized.

## To run server, execute:
`uvicorn servers.vicuna_server:app`

Access http://localhost:8000/docs for documentation on API

## Agent example:

`python -m langchain_app.agents.test_finetune`

## Medium Article
https://medium.com/@paolorechia/creating-my-first-ai-agent-with-vicuna-and-langchain-376ed77160e3

## Example run
https://gist.github.com/paolorechia/0b8b5e08b38040e7ec10eef237caf3a5
