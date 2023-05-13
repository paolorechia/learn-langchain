export USE_FINE_TUNED_LORA=true
export LORA_WEIGHTS=../vicuna-react-lora/lora-wizard-react_cut256_10epochs
export MODEL_PATH=TheBloke/wizardLM-7B-HF
uvicorn servers.vicuna_server:app
