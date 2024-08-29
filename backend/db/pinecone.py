from pinecone import Pinecone, ServerlessSpec
from config import Settings
from typing import List

settings = Settings()

class PineconeManager:
    def __init__(self):
        self.pinecone = Pinecone(api_key=settings.pinecone_api_key)
        self._create_index(settings.pinecone_index)

    def _create_index(self, index_name: str):
        if index_name not in self.pinecone.list_indexes().names():
            self.pinecone.create_index(
                name=index_name,
                dimension=768,
                metric="cosine", 
                spec=ServerlessSpec(
                    cloud="aws", 
                    region="us-east-1"
                ) 
            )

    def upsert_embeddings(self, index, embeddings: List[List[float]], ids: List[str], texts: List[str]):
        vectors = [
            (id, embedding, {"text": text}) 
            for id, embedding, text in zip(ids, embeddings, texts)
        ]
        index.upsert(vectors=vectors)


