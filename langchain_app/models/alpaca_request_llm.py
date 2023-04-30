from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

import requests

from langchain_app.utils.deprecation_warning import emit_module_deprecation_warning

emit_module_deprecation_warning(__name__)


class AlpacaLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = requests.post(
            "http://127.0.0.1:8000/prompt", json={"prompt": prompt}
        )
        response.raise_for_status()
        return response.json()["response"]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
