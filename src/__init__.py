"""
Hermes RAG - Domain-Driven RAG System

A comprehensive Retrieval-Augmented Generation system built with
Domain-Driven Design principles.
"""

from .domain.entities import Document, Chunk, Embedding, Query, SearchResult
from .domain.value_objects import (
    DocumentMetadata,
    DocumentStatus,
    SearchConfig,
    ChunkingConfig
)
from .application.use_cases import (
    IngestDocumentUseCase,
    SearchDocumentsUseCase,
    GenerateResponseUseCase
)

__version__ = "1.0.0"

__all__ = [
    "Document",
    "Chunk",
    "Embedding",
    "Query",
    "SearchResult",
    "DocumentMetadata",
    "DocumentStatus",
    "SearchConfig",
    "ChunkingConfig",
    "IngestDocumentUseCase",
    "SearchDocumentsUseCase",
    "GenerateResponseUseCase",
]
