"""Chunk Entity - Represents a text chunk from a document."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4


@dataclass
class Chunk:
    """
    Entity representing a text chunk extracted from a document.
    Contains normalized text and positional metadata for retrieval.
    """
    id: UUID = field(default_factory=uuid4)
    document_id: UUID = field(default_factory=uuid4)
    content: str = ""
    normalized_content: str = ""

    chunk_index: int = 0
    start_char: int = 0
    end_char: int = 0
    page_number: Optional[int] = None

    chunk_size: int = 512
    overlap_size: int = 50

    embedding_id: Optional[UUID] = None
    embedding_vector: Optional[List[float]] = None

    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def token_count(self) -> int:
        """Approximate token count (rough estimate)."""
        return len(self.normalized_content.split())

    @property
    def has_embedding(self) -> bool:
        """Check if chunk has been embedded."""
        return self.embedding_vector is not None

    def set_embedding(self, embedding_id: UUID, vector: List[float]) -> None:
        """Associate embedding with this chunk."""
        self.embedding_id = embedding_id
        self.embedding_vector = vector

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": str(self.id),
            "document_id": str(self.document_id),
            "content": self.content,
            "normalized_content": self.normalized_content,
            "chunk_index": self.chunk_index,
            "start_char": self.start_char,
            "end_char": self.end_char,
            "page_number": self.page_number,
            "chunk_size": self.chunk_size,
            "overlap_size": self.overlap_size,
            "has_embedding": self.has_embedding,
            "token_count": self.token_count,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Chunk":
        """Create chunk from dictionary."""
        return cls(
            id=UUID(data["id"]) if isinstance(data.get("id"), str) else data.get("id", uuid4()),
            document_id=UUID(data["document_id"]) if isinstance(data.get("document_id"), str) else data.get("document_id", uuid4()),
            content=data.get("content", ""),
            normalized_content=data.get("normalized_content", ""),
            chunk_index=data.get("chunk_index", 0),
            start_char=data.get("start_char", 0),
            end_char=data.get("end_char", 0),
            page_number=data.get("page_number"),
            chunk_size=data.get("chunk_size", 512),
            overlap_size=data.get("overlap_size", 50),
            metadata=data.get("metadata", {})
        )
