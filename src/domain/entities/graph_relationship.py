"""Graph Relationship - Represents an edge between entities in the knowledge graph."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List
from uuid import UUID, uuid4


@dataclass
class GraphRelationship:
    """
    Entity representing a directed edge in the knowledge graph.
    Connects two GraphEntity nodes with a typed relationship.
    """
    id: UUID = field(default_factory=uuid4)
    source_entity_id: UUID = field(default_factory=uuid4)
    target_entity_id: UUID = field(default_factory=uuid4)
    relationship_type: str = ""
    description: str = ""
    weight: float = 1.0

    source_chunk_ids: List[UUID] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def strengthen(self, additional_weight: float = 1.0) -> None:
        """Increase weight when same relationship is found again."""
        self.weight += additional_weight

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": str(self.id),
            "source_entity_id": str(self.source_entity_id),
            "target_entity_id": str(self.target_entity_id),
            "relationship_type": self.relationship_type,
            "description": self.description,
            "weight": self.weight,
            "source_chunk_ids": [str(cid) for cid in self.source_chunk_ids],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
