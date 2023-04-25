# GPTQ-for-LLaMA
NOTE: This directory is a direct clone of https://github.com/qwopqwop200/GPTQ-for-LLaMa, with very minor modifications. I DO NOT OWN this code.

4 bits quantization of [LLaMA](https://arxiv.org/abs/2302.13971) using [GPTQ](https://arxiv.org/abs/2210.17323)

GPTQ is SOTA one-shot weight quantization method

**Due to Triton's limitations, 3-bit is not supported. If you are using 3bit, please use [cuda branch](https://github.com/qwopqwop200/GPTQ-for-LLaMa/tree/cuda).**

**Triton only supports Linux, so if you are a Windows user, please use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).**

## News or Update
**I release [AutoGPTQ-triton](https://github.com/qwopqwop200/AutoGPTQ-triton), a packaged version of GPTQ based on [PanQiWei's AutoGPTQ](https://github.com/PanQiWei/AutoGPTQ). Use [AutoGPTQ](https://github.com/PanQiWei/AutoGPTQ) if you want a cuda version.**

## Result
<details>
<summary>LLaMA-7B(click me)</summary>

| [LLaMA-7B](https://arxiv.org/abs/2302.13971)       | Bits | group-size | memory(MiB) | Wikitext2 | checkpoint size(GB) |
| -------------------------------------------------- | ---- | ---------- | ----------- | --------- | ------------------- |
| FP16                                               |  16  |     -      |    13940    |    5.68   |         12.5        |
| RTN                                                |  4   |     -      |      -      |    6.29   |          -          |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  4   |     -      |     4740    |    6.09   |          3.5        |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  4   |    128     |     4891    |    5.85   |          3.6        |
| RTN                                                |  3   |     -      |      -      |   25.54   |          -          |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  3   |     -      |     3852    |    8.07   |          2.7        |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  3   |    128     |     4116    |    6.61   |          3.0        |

</details>

<details>
<summary>LLaMA-13B</summary>

| [LLaMA-13B](https://arxiv.org/abs/2302.13971)      | Bits | group-size | memory(MiB) | Wikitext2 | checkpoint size(GB) |
| -------------------------------------------------- | ---- | ---------- | ----------- | --------- | ------------------- |
| FP16                                               |  16  |     -      |     OOM     |    5.09   |         24.2        |
| RTN                                                |  4   |     -      |      -      |    5.53   |          -          |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  4   |     -      |     8410    |    5.36   |          6.5        |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  4   |    128     |     8747    |    5.20   |          6.7        |
| RTN                                                |  3   |     -      |      -      |   11.40   |          -          |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  3   |     -      |     6870    |    6.63   |          5.1        |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  3   |    128     |     7277    |    5.62   |          5.4        |

</details>

<details>
<summary>LLaMA-33B</summary>

| [LLaMA-33B](https://arxiv.org/abs/2302.13971)      | Bits | group-size | memory(MiB) | Wikitext2 | checkpoint size(GB) |
| -------------------------------------------------- | ---- | ---------- | ----------- | --------- | ------------------- |
| FP16                                               |  16  |     -      |     OOM     |    4.10   |         60.5        |
| RTN                                                |  4   |     -      |      -      |    4.54   |          -          |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  4   |     -      |    19493    |    4.45   |         15.7        |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  4   |    128     |    20570    |    4.23   |         16.3        |
| RTN                                                |  3   |     -      |      -      |   14.89   |          -          |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  3   |     -      |    15493    |    5.69   |         12.0        |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  3   |    128     |    16566    |    4.80   |         13.0        |

</details>

<details>
<summary>LLaMA-65B</summary>

| [LLaMA-65B](https://arxiv.org/abs/2302.13971)      | Bits | group-size | memory(MiB) | Wikitext2 | checkpoint size(GB) |
| -------------------------------------------------- | ---- | ---------- | ----------- | --------- | ------------------- |
| FP16                                               |  16  |     -      |     OOM     |    3.53   |         121.0       |
| RTN                                                |  4   |     -      |      -      |    3.92   |          -          |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  4   |     -      |     OOM     |    3.84   |         31.1        |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  4   |    128     |     OOM     |    3.65   |         32.3        |
| RTN                                                |  3   |     -      |      -      |   10.59   |          -          |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  3   |     -      |     OOM     |    5.04   |         23.6        |
| [GPTQ](https://arxiv.org/abs/2210.17323)           |  3   |    128     |     OOM     |    4.17   |         25.6        |
</details>

Quantization requires a large amount of CPU memory. However, the memory required can be reduced by using swap memory.

Depending on the GPUs/drivers, there may be a difference in performance, which decreases as the model size increases.(https://github.com/IST-DASLab/gptq/issues/1)

According to [GPTQ paper](https://arxiv.org/abs/2210.17323), As the size of the model increases, the difference in performance between FP16 and GPTQ decreases.

## Installation
If you don't have [conda](https://docs.conda.io/en/latest/miniconda.html), install it first.
```
conda create --name gptq python=3.9 -y
conda activate gptq
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
# Or, if you're having trouble with conda, use pip with python3.9:
# pip3 install torch torchvision torchaudio

git clone https://github.com/qwopqwop200/GPTQ-for-LLaMa
cd GPTQ-for-LLaMa
pip install -r requirements.txt
```
## Dependencies

* `torch`: tested on v2.0.0+cu117
* `transformers`: tested on v4.28.0.dev0
* `datasets`: tested on v2.10.1
* `safetensors`: tested on v0.3.0

All experiments were run on a single NVIDIA RTX3090.

# Language Generation
## LLaMA

```
#convert LLaMA to hf
python convert_llama_weights_to_hf.py --input_dir /path/to/downloaded/llama/weights --model_size 7B --output_dir ./llama-hf

# Benchmark language generation with 4-bit LLaMA-7B:

# Save compressed model
CUDA_VISIBLE_DEVICES=0 python llama.py ${MODEL_DIR} c4 --wbits 4 --true-sequential --act-order --groupsize 128 --save llama7b-4bit-128g.pt

# Or save compressed `.safetensors` model
CUDA_VISIBLE_DEVICES=0 python llama.py ${MODEL_DIR} c4 --wbits 4 --true-sequential --act-order --groupsize 128 --save_safetensors llama7b-4bit-128g.safetensors

# Benchmark generating a 2048 token sequence with the saved model
CUDA_VISIBLE_DEVICES=0 python llama.py ${MODEL_DIR} c4 --wbits 4 --groupsize 128 --load llama7b-4bit-128g.pt --benchmark 2048 --check

# Benchmark FP16 baseline, note that the model will be split across all listed GPUs
CUDA_VISIBLE_DEVICES=0,1,2,3,4 python llama.py ${MODEL_DIR} c4 --benchmark 2048 --check

# model inference with the saved model
CUDA_VISIBLE_DEVICES=7 python llama_inference.py ${MODEL_DIR} --load llama7b-4bit-128g.pt --text "this is llama"

# model inference with the saved model using safetensors loaded direct to gpu
CUDA_VISIBLE_DEVICES=0 python llama_inference.py ${MODEL_DIR} --load llama7b-4bit-128g.safetensors --text "this is llama" --device=0

# model inference with the saved model with offload(This is very slow. This is a simple implementation and could be improved with technologies like flexgen(https://github.com/FMInference/FlexGen).
CUDA_VISIBLE_DEVICES=0 python llama_inference_offload.py ${MODEL_DIR} --wbits 4 --groupsize 128 --load llama7b-4bit-128g.pt --text "this is llama" --pre_layer 16
It takes about 180 seconds to generate 45 tokens(5->50 tokens) on single RTX3090 based on LLaMa-65B. pre_layer is set to 50.
```
Basically, 4-bit quantization and 128 groupsize are recommended.

You can also export quantization parameters with toml+numpy format.
```
CUDA_VISIBLE_DEVICES=0 python llama.py ${MODEL_DIR} c4 --wbits 4 --true-sequential --act-order --groupsize 128 --quant-directory ${TOML_DIR}
```

# Acknowledgements
This code is based on [GPTQ](https://github.com/IST-DASLab/gptq)

Thanks to Meta AI for releasing [LLaMA](https://arxiv.org/abs/2302.13971), a powerful LLM.

Triton GPTQ kernel code is based on [GPTQ-triton](https://github.com/fpgaminer/GPTQ-triton)
