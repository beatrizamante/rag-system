"""
Configuration Module for Hermes RAG System.

Provides centralized configuration management using environment variables
and sensible defaults.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import os


@dataclass
class EmbeddingConfig:
    """Embedding service configuration."""
    model_name: str = "text-embedding-ada-002"
    dimensions: int = 1536
    batch_size: int = 100
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600


@dataclass
class ChunkingConfig:
    """Document chunking configuration."""
    chunk_size: int = 512
    chunk_overlap: int = 50
    min_chunk_size: int = 100
    max_chunk_size: int = 1000
    strategy: str = "recursive"  # fixed_size, sentence, paragraph, recursive


@dataclass
class SearchConfig:
    """Search configuration."""
    similarity_metric: str = "cosine"  # cosine, dot_product, euclidean
    search_type: str = "hybrid"  # vector, keyword, hybrid
    top_k: int = 10
    top_k_vector: int = 50
    top_k_keyword: int = 50
    vector_weight: float = 0.7
    keyword_weight: float = 0.3
    enable_reranking: bool = True
    rerank_top_k: int = 20
    rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"


@dataclass
class GenerationConfig:
    """LLM generation configuration."""
    model: str = "gpt-4"
    temperature: float = 0.0
    max_tokens: int = 1000
    max_context_tokens: int = 4000
    max_context_chunks: int = 5


@dataclass
class CacheConfig:
    """Caching configuration."""
    enable_memory_cache: bool = True
    enable_redis_cache: bool = False
    redis_url: str = "redis://localhost:6379"
    default_ttl_seconds: int = 3600
    max_memory_mb: int = 512


@dataclass
class AppConfig:
    """Main application configuration."""
    ai_api_key: str = ""

    vector_store_path: str = "./data/vectorstore"
    documents_path: str = "./data/documents"

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables."""
        return cls(
            ai_api_key=os.getenv("OPENAI_API_KEY", ""),
            vector_store_path=os.getenv("VECTOR_STORE_PATH", "./data/vectorstore"),
            documents_path=os.getenv("DOCUMENTS_PATH", "./data/documents"),
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            embedding=EmbeddingConfig(
                model_name=os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002"),
                batch_size=int(os.getenv("EMBEDDING_BATCH_SIZE", "100")),
                enable_caching=os.getenv("EMBEDDING_CACHE", "true").lower() == "true"
            ),
            chunking=ChunkingConfig(
                chunk_size=int(os.getenv("CHUNK_SIZE", "512")),
                chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "50")),
                strategy=os.getenv("CHUNK_STRATEGY", "recursive")
            ),
            search=SearchConfig(
                similarity_metric=os.getenv("SIMILARITY_METRIC", "cosine"),
                search_type=os.getenv("SEARCH_TYPE", "hybrid"),
                top_k=int(os.getenv("SEARCH_TOP_K", "10")),
                enable_reranking=os.getenv("ENABLE_RERANKING", "true").lower() == "true"
            ),
            generation=GenerationConfig(
                model=os.getenv("LLM_MODEL", "gpt-4"),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.0")),
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1000"))
            ),
            cache=CacheConfig(
                enable_memory_cache=os.getenv("ENABLE_CACHE", "true").lower() == "true",
                max_memory_mb=int(os.getenv("CACHE_MAX_MB", "512"))
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (hiding sensitive values)."""
        return {
            "ai_api_key": "***" if self.ai_api_key else "",
            "vector_store_path": self.vector_store_path,
            "host": self.host,
            "port": self.port,
            "debug": self.debug,
            "embedding": {
                "model": self.embedding.model_name,
                "batch_size": self.embedding.batch_size
            },
            "chunking": {
                "size": self.chunking.chunk_size,
                "overlap": self.chunking.chunk_overlap,
                "strategy": self.chunking.strategy
            },
            "search": {
                "metric": self.search.similarity_metric,
                "type": self.search.search_type,
                "top_k": self.search.top_k,
                "reranking": self.search.enable_reranking
            }
        }


_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get or create global configuration."""
    global _config
    if _config is None:
        _config = AppConfig.from_env()
    return _config


def set_config(config: AppConfig) -> None:
    """Set global configuration."""
    global _config
    _config = config
