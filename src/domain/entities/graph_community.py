"""Graph Community - Represents a cluster of related entities in the knowledge graph."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List
from uuid import UUID, uuid4


@dataclass
class GraphCommunity:
    """
    Entity representing a community (cluster) of related entities.
    Generated via community detection algorithms (e.g., Leiden).
    Each community has an LLM-generated summary for retrieval.
    """
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    summary: str = ""
    level: int = 0

    entity_ids: List[UUID] = field(default_factory=list)
    relationship_ids: List[UUID] = field(default_factory=list)

    source_document_ids: List[UUID] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def entity_count(self) -> int:
        """Number of entities in this community."""
        return len(self.entity_ids)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": str(self.id),
            "title": self.title,
            "summary": self.summary,
            "level": self.level,
            "entity_count": self.entity_count,
            "entity_ids": [str(eid) for eid in self.entity_ids],
            "source_document_ids": [str(did) for did in self.source_document_ids],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
