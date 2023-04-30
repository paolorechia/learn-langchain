export MODEL_PATH=wizardLM-7B-GPTQ
export MODEL_CHECKPOINT=wizardLM-7B-GPTQ-4bit.no-act-order.safetensors
export USE_4BIT=true
export USE_13B_MODEL=true
uvicorn servers.vicuna_server:app 