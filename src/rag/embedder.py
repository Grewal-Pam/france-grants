from typing import List, Union

import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    """
    Wrapper around a SentenceTransformer model.
    Responsibility:
    - Load the embedding model once
    - Provide a simple .encode(texts) method
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        """
        model_name:
            - 'all-MiniLM-L6-v2' is small, fast and good quality
            - works well on CPU and on a MacBook
        """
        print(f"[Embedder] Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Convert text(s) into vector embeddings.

        Input:
            - texts: a string or a list of strings
        Output:
            - numpy array of shape (N, D)
        """
        if isinstance(texts, str):
            texts = [texts]

        print(f"[Embedder] Encoding {len(texts)} texts...")
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        print(f"[Embedder] Output shape: {embeddings.shape}")
        return embeddings
