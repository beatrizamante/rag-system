"""Query Entity - Represents a search query in the RAG system."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from ..value_objects.search_config import SearchConfig


@dataclass
class Query:
    """
    Entity representing a user query for retrieval.
    Contains the query text and search configuration.
    """
    id: UUID = field(default_factory=uuid4)
    text: str = ""
    normalized_text: str = ""

    config: SearchConfig = field(default_factory=SearchConfig)

    embedding: Optional[List[float]] = None

    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.now)

    embedding_time_ms: float = 0.0
    search_time_ms: float = 0.0
    rerank_time_ms: float = 0.0
    total_time_ms: float = 0.0

    @property
    def has_embedding(self) -> bool:
        """Check if query has been embedded."""
        return self.embedding is not None

    def set_embedding(self, vector: List[float], time_ms: float) -> None:
        """Set the query embedding vector."""
        self.embedding = vector
        self.embedding_time_ms = time_ms

    def record_search_time(self, time_ms: float) -> None:
        """Record search execution time."""
        self.search_time_ms = time_ms

    def record_rerank_time(self, time_ms: float) -> None:
        """Record reranking time."""
        self.rerank_time_ms = time_ms

    def finalize_timing(self) -> None:
        """Calculate total execution time."""
        self.total_time_ms = (
            self.embedding_time_ms +
            self.search_time_ms +
            self.rerank_time_ms
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": str(self.id),
            "text": self.text,
            "config": self.config.to_dict(),
            "has_embedding": self.has_embedding,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "timing": {
                "embedding_ms": self.embedding_time_ms,
                "search_ms": self.search_time_ms,
                "rerank_ms": self.rerank_time_ms,
                "total_ms": self.total_time_ms
            },
            "created_at": self.created_at.isoformat()
        }
