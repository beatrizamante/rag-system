"""Search Result Entity - Represents retrieval results."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from .chunk import Chunk


@dataclass
class SearchResultItem:
    """Individual search result item."""
    chunk: Chunk
    score: float = 0.0

    vector_score: float = 0.0
    keyword_score: float = 0.0

    original_rank: int = 0
    reranked_score: Optional[float] = None
    final_rank: int = 0

    score_breakdown: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "chunk_id": str(self.chunk.id),
            "document_id": str(self.chunk.document_id),
            "content": self.chunk.content,
            "score": self.score,
            "vector_score": self.vector_score,
            "keyword_score": self.keyword_score,
            "original_rank": self.original_rank,
            "reranked_score": self.reranked_score,
            "final_rank": self.final_rank,
            "metadata": self.chunk.metadata
        }


@dataclass
class SearchResult:
    """
    Aggregate for search results.
    Contains ranked results and search metadata.
    """
    id: UUID = field(default_factory=uuid4)
    query_id: UUID = field(default_factory=uuid4)
    items: List[SearchResultItem] = field(default_factory=list)

    similarity_metric: str = "cosine"
    search_type: str = "hybrid"
    top_k: int = 10
    reranking_enabled: bool = True

    total_candidates: int = 0
    vector_search_time_ms: float = 0.0
    keyword_search_time_ms: float = 0.0
    rerank_time_ms: float = 0.0

    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def result_count(self) -> int:
        """Number of results returned."""
        return len(self.items)

    @property
    def top_result(self) -> Optional[SearchResultItem]:
        """Get the top-ranked result."""
        return self.items[0] if self.items else None

    def get_context_for_generation(self, max_tokens: int = 4000) -> str:
        """
        Get concatenated context for prompt grounding.
        Respects token limit for context window.
        """
        context_parts = []
        current_tokens = 0

        for item in self.items:
            chunk_tokens = len(item.chunk.content.split())
            if current_tokens + chunk_tokens > max_tokens:
                break

            context_parts.append(
                f"[Source {item.final_rank + 1}]\n{item.chunk.content}"
            )
            current_tokens += chunk_tokens

        return "\n\n".join(context_parts)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": str(self.id),
            "query_id": str(self.query_id),
            "result_count": self.result_count,
            "total_candidates": self.total_candidates,
            "search_config": {
                "similarity_metric": self.similarity_metric,
                "search_type": self.search_type,
                "top_k": self.top_k,
                "reranking_enabled": self.reranking_enabled
            },
            "timing": {
                "vector_search_ms": self.vector_search_time_ms,
                "keyword_search_ms": self.keyword_search_time_ms,
                "rerank_ms": self.rerank_time_ms
            },
            "items": [item.to_dict() for item in self.items],
            "created_at": self.created_at.isoformat()
        }
