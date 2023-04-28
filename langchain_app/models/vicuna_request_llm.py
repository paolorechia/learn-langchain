from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

import requests


class VicunaLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if isinstance(stop, list):
            stop = stop + ["Observation:", "Code Result:"]
        elif stop is None:
            stop = ["Code Result: "]

        print("Using stop ", stop)
        response = requests.post(
            "http://127.0.0.1:8000/prompt",
            json={
                "prompt": prompt,
                "temperature": 0,
                "max_new_tokens": 64,
                "stop": stop,
            },
        )
        response.raise_for_status()
        return response.json()["response"]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
