"""Document Entity - Represents a source document in the RAG system."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4

from ..value_objects.metadata import DocumentMetadata
from ..value_objects.document_status import DocumentStatus


@dataclass
class Document:
    """
    Aggregate root for document processing.
    Handles the lifecycle of a document from ingestion to chunking.
    """
    id: UUID = field(default_factory=uuid4)
    filename: str = ""
    content: str = ""
    raw_content: bytes = b""
    metadata: DocumentMetadata = field(default_factory=DocumentMetadata)
    status: DocumentStatus = DocumentStatus.PENDING
    chunk_ids: List[UUID] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None

    is_broken: bool = False
    extraction_method: str = "default"

    def mark_as_processing(self) -> None:
        """Mark document as being processed."""
        self.status = DocumentStatus.PROCESSING
        self.updated_at = datetime.utcnow()

    def mark_as_processed(self, chunk_ids: List[UUID]) -> None:
        """Mark document as successfully processed."""
        self.status = DocumentStatus.PROCESSED
        self.chunk_ids = chunk_ids
        self.updated_at = datetime.utcnow()

    def mark_as_failed(self, error: str) -> None:
        """Mark document as failed during processing."""
        self.status = DocumentStatus.FAILED
        self.error_message = error
        self.updated_at = datetime.utcnow()

    def mark_as_broken(self, fallback_method: str) -> None:
        """Flag document as broken PDF requiring fallback extraction."""
        self.is_broken = True
        self.extraction_method = fallback_method
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": str(self.id),
            "filename": self.filename,
            "metadata": self.metadata.to_dict(),
            "status": self.status.value,
            "chunk_count": len(self.chunk_ids),
            "is_broken": self.is_broken,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "error_message": self.error_message
        }
