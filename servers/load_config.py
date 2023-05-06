import os


class Config:
    def __init__(self) -> None:
        self.base_model_size = "13b" if os.getenv("USE_13B_MODEL") == 'true' else "7b"
        self.use_4bit = True if os.getenv("USE_4BIT") == 'true' else False
        self.use_8bit = True if os.getenv("USE_8BIT") == 'true' else False
        self.use_fine_tuned_lora = True if os.getenv("USE_FINE_TUNED_LORA") == 'true' else False
        self.lora_weights = os.getenv("LORA_WEIGHTS")
        self.device = "cpu" if os.getenv("USE_CPU")== 'true' else "cuda"
        self.model_path = os.getenv("MODEL_PATH")
        self.model_checkpoint = os.getenv("MODEL_CHECKPOINT")

    def __str__(self) -> str:
        return str(self.__dict__)
