import random
from typing import List
from .base import BaseEmbedding

class EmbeddingService(BaseEmbedding):
    VECTOR_SIZE = 128

    def embed(self, text: str):
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.VECTOR_SIZE)]  