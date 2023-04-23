from langchain.embeddings.base import Embeddings
from pydantic import BaseModel
from typing import List, Optional
import requests


class VicunaEmbeddings(BaseModel, Embeddings):
    embedding_ctx_length: int = 8191
    chunk_size: int = 1000

    def _call(self, prompt: str) -> str:
        p = prompt.strip()
        print("Sending prompt ", p)
        response = requests.post(
            "http://127.0.0.1:8000/embedding",
            json={
                "prompt": p,
            }
        )
        response.raise_for_status()
        return response.json()["response"]


    def embed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        """Call out to OpenAI's embedding endpoint for embedding search docs.

        Args:
            texts: The list of texts to embed.
            chunk_size: The chunk size of embeddings. If None, will use the chunk size
                specified by the class.

        Returns:
            List of embeddings, one for each text.
        """
        results = []
        for text in texts:
            response = self.embed_query(
                text
            )
            results.append(response)
        return results

    def embed_query(self, text) -> List[float]:
        """Call out to OpenAI's embedding endpoint for embedding query text.

        Args:
            text: The text to embed.

        Returns:
            Embedding for the text.
        """
        embedding = self._call(text)
        return embedding
