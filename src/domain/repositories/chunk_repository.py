"""Chunk Repository Interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.chunk import Chunk


class ChunkRepository(ABC):
    """
    Abstract repository for chunk persistence.
    Manages storage of document chunks.
    """

    @abstractmethod
    async def save(self, chunk: Chunk) -> Chunk:
        """Persist a single chunk."""

    @abstractmethod
    async def save_batch(self, chunks: List[Chunk]) -> List[Chunk]:
        """Persist multiple chunks efficiently."""

    @abstractmethod
    async def get_by_id(self, chunk_id: UUID) -> Optional[Chunk]:
        """Retrieve chunk by ID."""

    @abstractmethod
    async def get_by_document_id(self, document_id: UUID) -> List[Chunk]:
        """Get all chunks for a document."""

    @abstractmethod
    async def get_by_ids(self, chunk_ids: List[UUID]) -> List[Chunk]:
        """Retrieve multiple chunks by IDs."""

    @abstractmethod
    async def delete_by_document_id(self, document_id: UUID) -> int:
        """Delete all chunks for a document. Returns count deleted."""

    @abstractmethod
    async def update_embedding(
        self,
        chunk_id: UUID,
        embedding_id: UUID,
        vector: List[float]
    ) -> bool:
        """Update chunk with embedding reference."""

    @abstractmethod
    async def get_chunks_without_embeddings(
        self,
        limit: int = 100
    ) -> List[Chunk]:
        """Get chunks that need embedding generation."""

    @abstractmethod
    async def count_by_document(self, document_id: UUID) -> int:
        """Count chunks for a specific document."""
