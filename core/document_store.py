from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from config import settings

class DocumentStore():
    def __init__(self, embedder, collection_name: str):
        self.client = QdrantClient(settings.qdrant_url, port=settings.port)
        self.embedder = embedder
        self.collection_name = collection_name
        self.docs_memory: List[str] = []

        if self.client:
            self._collection_exist()

    @property
    def document_count(self) -> int:
        return len(self.docs_memory)

    def _collection_exist(self):
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=128, distance=Distance.COSINE)
            )
                
        except Exception as e:
            self.client = None 
            print("⚠️  Qdrant not available. Falling back to in-memory list.")

    def add_document(self, text: str):
        doc_id = len(self.docs_memory)
        embedding = self.embedder.embed(text)
        payload = {"text": text}
        
        if self.client:
            self.client.upsert(
                collection_name=settings.collection_name,
                points=[PointStruct(id=doc_id, vector=embedding, payload=payload)]
            )
        else:
            self.docs_memory.append(text)
        return doc_id
    
    def search(self, query: str) -> List[str]:
        results = []
        embedding = self.embedder.embed(query)

        if self.client:
            hits = self.client.search(collection_name=settings.collection_name, query_vector=embedding, limit=2)
            for hit in hits:
                results.append(hit.payload["text"])
        else:
            for doc in self.docs_memory:
                if query.lower() in doc.lower():
                    results.append(doc)
            if not results and self.docs_memory:
                results = [self.docs_memory[0]] 
        return results