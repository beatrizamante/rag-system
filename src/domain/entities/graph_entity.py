"""Graph Entity - Represents a named entity extracted from document chunks."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4


@dataclass
class GraphEntity:
    """
    Entity representing a node in the knowledge graph.
    Extracted from document chunks via LLM-based entity extraction.
    """
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    entity_type: str = ""
    description: str = ""

    source_chunk_ids: List[UUID] = field(default_factory=list)
    source_document_ids: List[UUID] = field(default_factory=list)

    community_id: Optional[UUID] = None
    degree: int = 0

    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def canonical_name(self) -> str:
        """Lowercase canonical form for deduplication."""
        return self.name.strip().lower()

    def merge_with(self, other: "GraphEntity") -> None:
        """Merge another entity instance into this one (deduplication)."""
        for cid in other.source_chunk_ids:
            if cid not in self.source_chunk_ids:
                self.source_chunk_ids.append(cid)
        for did in other.source_document_ids:
            if did not in self.source_document_ids:
                self.source_document_ids.append(did)
        if other.description and len(other.description) > len(self.description):
            self.description = other.description

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": str(self.id),
            "name": self.name,
            "entity_type": self.entity_type,
            "description": self.description,
            "source_chunk_ids": [str(cid) for cid in self.source_chunk_ids],
            "source_document_ids": [str(did) for did in self.source_document_ids],
            "community_id": str(self.community_id) if self.community_id else None,
            "degree": self.degree,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
