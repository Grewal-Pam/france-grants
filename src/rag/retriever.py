from typing import List, Dict

from chromadb import PersistentClient
from .embedder import Embedder


class Retriever:
    """
    Retrieves the top-k most relevant documents from ChromaDB
    for a given natural language query.
    """

    def __init__(
        self,
        persist_dir: str = "vector_store",
        collection_name: str = "france_grants",
    ) -> None:
        print(f"[Retriever] Connecting to Chroma at {persist_dir}, collection={collection_name}")

        # NEW Chroma API
        self.client = PersistentClient(path=persist_dir)
        self.collection = self.client.get_collection(collection_name)

        # Use the SAME embedding model that built the index
        self.embedder = Embedder()

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Convert query → embedding → perform vector search.
        Returns: top-k docs with id, text, distance, metadata.
        """
        print(f"[Retriever] Searching for: {query!r} (top {k})")

        q_emb = self.embedder.encode(query)[0]

        results = self.collection.query(
            query_embeddings=[q_emb.tolist()],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        docs = []
        for doc_id, doc, dist, meta in zip(
            results["ids"][0],
            results["documents"][0],
            results["distances"][0],
            results["metadatas"][0],
        ):
            docs.append(
                {
                    "id": doc_id,
                    "text": doc,
                    "metadata": meta,
                    "distance": dist,
                }
            )

        print(f"[Retriever] Found {len(docs)} results.")
        return docs
