import os
from typing import List

import chromadb
import pandas as pd
from chromadb.config import Settings

from .embedder import Embedder
from chromadb import PersistentClient

DATA_SOURCES = [
    ("kg/nodes.csv", "kg_nodes"),
    ("kg/edges.csv", "kg_edges"),
    ("kg/edges_health_africa.csv", "kg_edges_health_africa"),
    ("analysis/summary_stats.csv", "summary_stats"),
]


class IndexBuilder:
    """
    Builds a ChromaDB vector index from:
    - kg/nodes.csv
    - kg/edges.csv
    - analysis/summary_stats.csv

    It:
    - Loads the CSVs
    - Creates a text representation per row
    - Embeds them
    - Saves them in a Chroma collection
    """

    def __init__(
        self,
        persist_dir: str = "vector_store",
        collection_name: str = "france_grants",
    ) -> None:
        self.persist_dir = persist_dir
        self.collection_name = collection_name

        print(f"[IndexBuilder] Using persist dir: {self.persist_dir}")
        os.makedirs(self.persist_dir, exist_ok=True)

        # Init Chroma client
        self.client = PersistentClient(path=self.persist_dir)

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "France health grants RAG store"},
        )

        self.embedder = Embedder()

    def load_sources(self) -> pd.DataFrame:
        """
        Load all configured CSV sources, attach a 'source' column,
        and concatenate into one DataFrame.
        """
        frames: List[pd.DataFrame] = []

        for path, label in DATA_SOURCES:
            if not os.path.exists(path):
                print(f"[IndexBuilder] WARNING: {path} not found, skipping.")
                continue

            print(f"[IndexBuilder] Loading {path} as source='{label}'")
            df = pd.read_csv(path)
            df["__source"] = label
            frames.append(df)

        if not frames:
            raise RuntimeError("[IndexBuilder] No data sources found.")

        df_all = pd.concat(frames, ignore_index=True)
        print(f"[IndexBuilder] Total rows loaded: {len(df_all)}")
        return df_all

    def build(self) -> None:
        """
        Main method:
        - loads data
        - converts rows to text
        - embeds them
        - writes to Chroma collection
        """
        df = self.load_sources()

        # Turn each row into a text block
        print("[IndexBuilder] Converting rows to text documents...")
        texts: List[str] = []
        metadatas: List[dict] = []
        ids: List[str] = []

        for idx, row in df.iterrows():
            # Simple text representation: "col1: value1; col2: value2; ..."
            parts = [f"{col}: {row[col]}" for col in df.columns if col != "__source"]
            text = " | ".join(parts)

            texts.append(text)
            metadatas.append(
                {
                    "source": row["__source"],
                }
            )
            ids.append(f"doc_{idx}")

        print(f"[IndexBuilder] Created {len(texts)} documents.")

        embeddings = self.embedder.encode(texts)

        print("[IndexBuilder] Adding embeddings to Chroma collection...")

        self.collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
        )

        print("[IndexBuilder] ✅ Index build complete. Collection stored at:", self.persist_dir)


def main() -> None:
    builder = IndexBuilder()
    builder.build()


if __name__ == "__main__":
    main()
