"""Search Configuration Value Object."""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class SimilarityMetric(Enum):
    """
    Similarity metrics for vector search.

    COSINE: Best for normalized vectors, measures angle between vectors.
            Recommended for most text embedding models.
            Range: -1 to 1 (1 = identical)

    DOT_PRODUCT: Best for magnitude-aware comparisons.
                 Faster computation but requires normalized vectors for fair comparison.
                 Range: unbounded

    EUCLIDEAN: Measures actual distance. Lower = more similar.
               Good for dense, low-dimensional embeddings.
    """
    COSINE = "cosine"
    DOT_PRODUCT = "dot_product"
    EUCLIDEAN = "euclidean"


class SearchType(Enum):
    """Search strategy types."""
    VECTOR = "vector"
    KEYWORD = "keyword"
    HYBRID = "hybrid"


@dataclass(frozen=True)
class SearchConfig:
    """
    Immutable configuration for search operations.
    Controls retrieval behavior and ranking.
    """
    similarity_metric: SimilarityMetric = SimilarityMetric.COSINE

    search_type: SearchType = SearchType.HYBRID

    top_k: int = 10
    top_k_vector: int = 50
    top_k_keyword: int = 50

    vector_weight: float = 0.7
    keyword_weight: float = 0.3

    enable_reranking: bool = True
    rerank_top_k: int = 20
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    min_score_threshold: float = 0.0
    filter_metadata: Optional[Dict[str, Any]] = None

    max_context_tokens: int = 4000
    max_context_chunks: int = 5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "similarity_metric": self.similarity_metric.value,
            "search_type": self.search_type.value,
            "top_k": self.top_k,
            "top_k_vector": self.top_k_vector,
            "top_k_keyword": self.top_k_keyword,
            "vector_weight": self.vector_weight,
            "keyword_weight": self.keyword_weight,
            "enable_reranking": self.enable_reranking,
            "rerank_top_k": self.rerank_top_k,
            "rerank_model": self.rerank_model,
            "min_score_threshold": self.min_score_threshold,
            "max_context_tokens": self.max_context_tokens,
            "max_context_chunks": self.max_context_chunks
        }

    @classmethod
    def default_for_qa(cls) -> "SearchConfig":
        """Optimized config for Q&A use cases - precision focused."""
        return cls(
            similarity_metric=SimilarityMetric.COSINE,
            search_type=SearchType.HYBRID,
            top_k=5,
            enable_reranking=True,
            max_context_chunks=3
        )

    @classmethod
    def default_for_research(cls) -> "SearchConfig":
        """Optimized config for research - recall focused."""
        return cls(
            similarity_metric=SimilarityMetric.COSINE,
            search_type=SearchType.HYBRID,
            top_k=20,
            top_k_vector=100,
            top_k_keyword=100,
            enable_reranking=True,
            rerank_top_k=50,
            max_context_chunks=10
        )
