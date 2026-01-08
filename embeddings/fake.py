import random
from typing import List
from .base import BaseEmbedding

class FakeEmbedding(BaseEmbedding):
    VECTOR_SIZE = 128

    def embed(self, text: str):
        # Seed based on input so it's "deterministic"
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.VECTOR_SIZE)]  # Small vector for demo