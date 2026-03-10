"""Embedding Repository Interface."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from ..entities.embedding import Embedding


class EmbeddingRepository(ABC):
    """
    Abstract repository for embedding persistence.
    Manages storage of vector embeddings.
    """

    @abstractmethod
    async def save(self, embedding: Embedding) -> Embedding:
        """Persist an embedding."""

    @abstractmethod
    async def save_batch(self, embeddings: List[Embedding]) -> List[Embedding]:
        """Persist multiple embeddings efficiently."""

    @abstractmethod
    async def get_by_id(self, embedding_id: UUID) -> Optional[Embedding]:
        """Retrieve embedding by ID."""

    @abstractmethod
    async def get_by_chunk_id(self, chunk_id: UUID) -> Optional[Embedding]:
        """Get embedding for a specific chunk."""

    @abstractmethod
    async def get_by_chunk_ids(self, chunk_ids: List[UUID]) -> List[Embedding]:
        """Get embeddings for multiple chunks."""

    @abstractmethod
    async def delete_by_chunk_id(self, chunk_id: UUID) -> bool:
        """Delete embedding for a chunk."""

    @abstractmethod
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get embedding cache statistics."""
