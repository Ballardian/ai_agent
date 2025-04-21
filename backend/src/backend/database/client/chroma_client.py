import chromadb

# see https://github.com/chroma-core/chroma/issues/2555
from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import (
    ONNXMiniLM_L6_V2,
)

from src.backend.database.client.indexed_content import IndexedContent

ef = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])


class ChromaClient:
    def __init__(self, collection_name: str, path: str = ".ai_agent_chroma_db"):
        print(f"Initializing ChromaClient with path: {path}")
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            collection_name, embedding_function=ef
        )

    def add_content(
        self,
        indexed_content: IndexedContent,
    ):
        content_dict = indexed_content.to_dict()
        metadata = {
            "name": content_dict["name"],
            "source": content_dict["source"],
            "date": content_dict["date"],
            "subject": content_dict["subject"],
        }
        self.collection.upsert(
            documents=[content_dict["content"]],
            ids=[content_dict["id"]],
            metadatas=[metadata],
        )

    def fetch_content(
        self, query_texts: list[str], n_results: int = 3, where: dict = None
    ):
        return self.collection.query(
            query_texts=query_texts, n_results=n_results, where=where
        )

    def get_all_documents(self):
        return self.collection.get()
