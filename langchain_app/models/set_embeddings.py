from langchain.embeddings.base import Embeddings
from pydantic import BaseModel
from typing import List, Optional

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embedding_ctx_length: int = 8191
chunk_size: int = 1000

class SentenceTransformerEmbeddings(BaseModel, Embeddings):
    def embed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        """Use a sentence transformer model to extract embeddings.

        Args:
            texts: The list of texts to embed.
            chunk_size: The chunk size of embeddings. If None, will use the chunk size
                specified by the class.

        Returns:
            List of embeddings, one for each text.
        """
        encoded_texts = model.encode(texts)
        result = []
        for encoded in encoded_texts:
            embedding = [
                float(x) for x in encoded
            ]
            result.append(embedding)
        return result

    def embed_query(self, text) -> List[float]:
        """Use a sentence transformer model to extract embeddings from query.

        Args:
            text: The text to embed.

        Returns:
            Embedding for the text.
        """
        embedding = [float(x)for x in model.encode(text)]
        return embedding