"""Document Metadata Value Object."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List


@dataclass(frozen=True)
class DocumentMetadata:
    """
    Immutable value object for document metadata.
    Contains all metadata extracted from the source document.
    """
    title: Optional[str] = None
    author: Optional[str] = None
    source: Optional[str] = None
    file_type: str = "unknown"
    file_size_bytes: int = 0
    page_count: Optional[int] = None
    language: str = "en"

    # Extraction metadata
    extraction_date: datetime = field(default_factory=datetime.utcnow)
    extraction_method: str = "default"

    # Custom metadata
    tags: tuple = field(default_factory=tuple)  # Immutable sequence
    custom_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "title": self.title,
            "author": self.author,
            "source": self.source,
            "file_type": self.file_type,
            "file_size_bytes": self.file_size_bytes,
            "page_count": self.page_count,
            "language": self.language,
            "extraction_date": self.extraction_date.isoformat(),
            "extraction_method": self.extraction_method,
            "tags": list(self.tags),
            "custom_fields": self.custom_fields
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentMetadata":
        """Create from dictionary."""
        return cls(
            title=data.get("title"),
            author=data.get("author"),
            source=data.get("source"),
            file_type=data.get("file_type", "unknown"),
            file_size_bytes=data.get("file_size_bytes", 0),
            page_count=data.get("page_count"),
            language=data.get("language", "en"),
            extraction_method=data.get("extraction_method", "default"),
            tags=tuple(data.get("tags", [])),
            custom_fields=data.get("custom_fields", {})
        )
