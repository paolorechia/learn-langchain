export MODEL_PATH=renamed-vicuna-7B-1.1-GPTQ-4bit-128g
export MODEL_CHECKPOINT=vicuna-7B-1.1-GPTQ-4bit-128g.safetensors
export USE_4BIT=true
export USE_7B_MODEL=true
uvicorn servers.vicuna_server:app 