from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from embeddings.fake import FakeEmbedding
from config import settings

class RAG():
    def __init__(self):
        self.client = QdrantClient(settings.qdrant_url, port=settings.port)
        self.embedder = FakeEmbedding()
        self.docs_memory: List[str] = []
        self._collection_exist()

    @property
    def document_count(self) -> int:
        return len(self.docs_memory)

    def _collection_exist(self):
        try:
            self.client.recreate_collection(
                    collection_name=settings.collection_name,
                    vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
                
        except Exception as e:
            self.client = None 
            print("⚠️  Qdrant not available. Falling back to in-memory list.")

    def add_document(self, text: str):
        doc_id = len(self.docs_memory)  # super unsafe ID!
        
        if self.client:
            emb = self.embedder.embed(text)
            payload = {"text": text}
            self.client.upsert(
                collection_name=settings.collection_name,
                points=[PointStruct(id=doc_id, vector=emb, payload=payload)]
            )
        else:
            self.docs_memory.append(text)
        return doc_id
    
    def search(self, query: str) -> List[str]:
        results = []
        emb = self.embedder.embed(query)

        if self.client:
            hits = self.client.search(collection_name=settings.collection_name, query_vector=emb, limit=2)
            for hit in hits:
                results.append(hit.payload["text"])
        else:
            for doc in self.docs_memory:
                if query.lower() in doc.lower():
                    results.append(doc)
            if not results and self.docs_memory:
                results = [self.docs_memory[0]]  # Just grab first
        return results