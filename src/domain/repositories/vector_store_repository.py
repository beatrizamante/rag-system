"""Vector Store Repository Interface."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID

from ..value_objects.search_config import SearchConfig, SimilarityMetric

class VectorStoreRepository(ABC):
    """
    Abstract repository for vector similarity search.
    Handles vector indexing and retrieval operations.
    """

    @abstractmethod
    async def index_vectors(
        self,
        vectors: List[Tuple[UUID, List[float], Dict[str, Any]]]
    ) -> int:
        """
        Index vectors with their IDs and metadata.
        Returns count of indexed vectors.

        Args:
            vectors: List of (chunk_id, vector, metadata) tuples
        """

    @abstractmethod
    async def search_vectors(
        self,
        query_vector: List[float],
        top_k: int = 10,
        similarity_metric: SimilarityMetric = SimilarityMetric.COSINE,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[UUID, float]]:
        """
        Search for similar vectors.

        Returns:
            List of (chunk_id, similarity_score) tuples
        """

    @abstractmethod
    async def hybrid_search(
        self,
        query_vector: List[float],
        query_text: str,
        config: SearchConfig
    ) -> List[Tuple[UUID, float, float]]:
        """
        Perform hybrid vector + keyword search.

        Returns:
            List of (chunk_id, vector_score, keyword_score) tuples
        """

    @abstractmethod
    async def delete_vectors(self, chunk_ids: List[UUID]) -> int:
        """Delete vectors by chunk IDs. Returns count deleted."""

    @abstractmethod
    async def update_vector(
        self,
        chunk_id: UUID,
        vector: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update an existing vector."""

    @abstractmethod
    async def get_index_stats(self) -> Dict[str, Any]:
        """Get vector index statistics."""

    @abstractmethod
    async def optimize_index(self) -> bool:
        """Optimize the vector index for better search performance."""
