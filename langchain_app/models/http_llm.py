from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Union, Any, Callable
from pydantic import Field
from typing import Dict
import requests
from copy import deepcopy


def default_extractor(json_response: Dict[str, Any], stop_parameter_name) -> str:
    return json_response["response"]


class HTTPBaseLLM(LLM):
    prompt_url: str
    parameters: Dict[str, Union[float, int, str, bool, List[str]]] = Field(
        default_factory=dict
    )
    response_extractor: Callable[[Dict[str, Any]], str] = default_extractor
    stop_parameter_name: str = "stop"

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Merge passed stop list with class parameters
        if isinstance(stop, list):
            stop_list = list(
                set(stop).union(set(self.parameters[self.stop_parameter_name]))
            )

        params = deepcopy(self.parameters)
        params[self.stop_parameter_name] = stop_list

        response = requests.post(
            self.prompt_url,
            json={
                "prompt": prompt,
                **params,
            },
        )
        response.raise_for_status()
        return self.response_extractor(response.json(), self.stop_parameter_name)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
