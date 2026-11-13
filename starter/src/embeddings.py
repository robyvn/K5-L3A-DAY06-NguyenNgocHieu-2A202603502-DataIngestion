"""Embedding provider adapter using sentence-transformers."""
from typing import Protocol
import torch
from sentence_transformers import SentenceTransformer


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, question: str) -> list[float]:
        ...


class MyEmbedder:
    """Embedder implementation using local SentenceTransformer models."""

    def __init__(self, model_name: str = "google/embeddinggemma-2", batch_size: int = 32) -> None:
        self.model_name = model_name
        self.batch_size = batch_size
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load model with float32 on CPU for optimal speed
        model_kwargs = {}
        if device == "cpu":
            model_kwargs["dtype"] = torch.float32
            
        self.model = SentenceTransformer(
            model_name,
            device=device,
            model_kwargs=model_kwargs
        )
        
        # Determine vector dimensionality
        test_emb = self.model.encode("test", normalize_embeddings=True)
        self.dimensions = int(len(test_emb))

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one normalized vector per input text in order."""
        if not texts:
            return []
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embeddings.tolist()

    def embed_query(self, question: str) -> list[float]:
        """Return a normalized query vector."""
        embedding = self.model.encode(
            question,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embedding.tolist()
