"""Chunking Configuration Value Object."""
from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class ChunkingStrategy(Enum):
    """
    Chunking strategies for document processing.

    FIXED_SIZE: Split by character count with overlap.
                Simple, fast, but may break mid-sentence.

    SENTENCE: Split by sentences, respecting natural boundaries.
              Better semantic coherence, variable chunk sizes.

    PARAGRAPH: Split by paragraphs.
               Best for structured documents.

    SEMANTIC: Use embeddings to find semantic boundaries.
              Highest quality but computationally expensive.

    RECURSIVE: Recursively split using hierarchy of separators.
               Good balance of speed and quality.
    """
    FIXED_SIZE = "fixed_size"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"


@dataclass(frozen=True)
class ChunkingConfig:
    """
    Immutable configuration for text chunking.
    Controls how documents are split into retrievable units.
    """
    strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE

    chunk_size: int = 512  # Target size in characters
    chunk_overlap: int = 50  # Overlap between chunks
    min_chunk_size: int = 100  # Minimum chunk size
    max_chunk_size: int = 1000  # Maximum chunk size

    # Token-based limits (more accurate for LLM context)
    use_token_counting: bool = True
    target_tokens: int = 256
    max_tokens: int = 512

    # Separator configuration for recursive strategy
    separators: tuple = ("\n\n", "\n", ". ", " ", "")

    # Text normalization
    normalize_whitespace: bool = True
    normalize_unicode: bool = True
    remove_special_chars: bool = False
    lowercase: bool = False

    # Metadata preservation
    preserve_metadata: bool = True
    include_page_numbers: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "strategy": self.strategy.value,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "min_chunk_size": self.min_chunk_size,
            "max_chunk_size": self.max_chunk_size,
            "use_token_counting": self.use_token_counting,
            "target_tokens": self.target_tokens,
            "max_tokens": self.max_tokens,
            "separators": list(self.separators),
            "normalize_whitespace": self.normalize_whitespace,
            "normalize_unicode": self.normalize_unicode,
            "remove_special_chars": self.remove_special_chars,
            "lowercase": self.lowercase
        }

    @classmethod
    def for_qa(cls) -> "ChunkingConfig":
        """Config optimized for Q&A - smaller, focused chunks."""
        return cls(
            chunk_size=300,
            chunk_overlap=50,
            target_tokens=150,
            max_tokens=300
        )

    @classmethod
    def for_summarization(cls) -> "ChunkingConfig":
        """Config optimized for summarization - larger chunks."""
        return cls(
            chunk_size=1000,
            chunk_overlap=100,
            target_tokens=500,
            max_tokens=750
        )

    @classmethod
    def for_code(cls) -> "ChunkingConfig":
        """Config optimized for code documents."""
        return cls(
            strategy=ChunkingStrategy.RECURSIVE,
            chunk_size=500,
            chunk_overlap=100,
            separators=("\n\nclass ", "\n\ndef ", "\n\n", "\n", " "),
            normalize_whitespace=False,  # Preserve code formatting
            lowercase=False
        )
