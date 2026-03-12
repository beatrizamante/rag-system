"""RAG System configuration module using Pydantic Settings for environment variable management."""

from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    LLM_API_KEY: SecretStr = Field(default="your-api-key-here", description="API key for the LLM provider (e.g., OpenAI, DeepSeek)")

    HOST: str = Field(default="0.0.0.0", description="Host address for the server")
    PORT: int = Field(default=8000, description="Port number for the server")
    DEBUG: bool = Field(default=False, description="Enable debug mode for verbose logging")

    VECTOR_STORE_PATH: str = Field(default="./data/vectorstore", description="Directory path for storing vector embeddings")
    DOCUMENTS_PATH: str = Field(default="./data/documents", description="Directory path for source documents")

    EMBEDDING_MODEL: str = Field(default="text-embedding-ada-002", description="Model name for generating embeddings")
    EMBEDDING_BATCH_SIZE: int = Field(default=100, description="Number of texts to embed per batch")
    EMBEDDING_CACHE: bool = Field(default=True, description="Enable caching for computed embeddings")

    CHUNK_SIZE: int = Field(default=512, description="Maximum number of tokens per text chunk")
    CHUNK_OVERLAP: int = Field(default=15, description="Percentage of overlapping tokens between consecutive chunks")
    CHUNK_STRATEGY: Literal["recursive", "fixed", "semantic"] = Field(default="recursive", description="Text chunking strategy (e.g., 'recursive', 'fixed', 'semantic')")

    SIMILARITY_METRIC: Literal["cosine", "dot-product", "euclidean"] = Field(default="cosine", description="Metric for computing vector similarity (e.g., 'cosine', 'euclidean', 'dot')")

    SEARCH_TYPE: Literal["semantic", "keyword", "hybrid"] = Field(default="hybrid", description="Search method (e.g., 'semantic', 'keyword', 'hybrid')")
    SEARCH_TOP_K: int = Field(default=10, description="Number of top results to return from search")
    ENABLE_RERANKING: bool = Field(default=True, description="Enable reranking of search results for improved relevance")

    LLM_MODEL: str = Field(default="gpt-4", description="LLM model name for response generation")
    LLM_TEMPERATURE: float = Field(default=0.0, description="Temperature for LLM response randomness (0.0 = deterministic)")
    LLM_MAX_TOKENS: int = Field(default=1000, description="Maximum tokens in LLM response")

    ENABLE_CACHE: bool = Field(default=True, description="Enable response caching")
    CACHE_MAX_MB: int = Field(default=512, description="Maximum cache size in megabytes")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
