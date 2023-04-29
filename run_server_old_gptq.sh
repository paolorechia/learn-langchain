export USE_4BIT=true
export USE_13B_MODEL=true
export MODEL_PATH=vicuna-13B-1.1-GPTQ-4bit-128g
export MODEL_CHECKPOINT=vicuna-13B-1.1-GPTQ-4bit-128g.no-act-order.pt
uvicorn servers.vicuna_server:app 