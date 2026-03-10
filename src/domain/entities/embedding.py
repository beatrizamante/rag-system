"""Embedding Entity - Represents vector embeddings."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4

import math



@dataclass
class Embedding:
    """
    Entity representing a vector embedding.
    Stores the vector and metadata about its generation.
    """
    id: UUID = field(default_factory=uuid4)
    chunk_id: UUID = field(default_factory=uuid4)
    vector: List[float] = field(default_factory=list)

    model_name: str = "text-embedding-ada-002"
    model_version: str = "1.0"
    dimensions: int = 1536

    generation_time_ms: float = 0.0
    cached: bool = False
    batch_id: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_valid(self) -> bool:
        """Check if embedding vector is valid."""
        return len(self.vector) == self.dimensions and all(
            isinstance(v, (int, float)) for v in self.vector
        )

    @property
    def magnitude(self) -> float:
        """Calculate vector magnitude for normalization."""
        return math.sqrt(sum(v * v for v in self.vector))

    def normalize(self) -> List[float]:
        """Return L2 normalized vector (for cosine similarity)."""
        mag = self.magnitude
        if mag == 0:
            return self.vector
        return [v / mag for v in self.vector]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": str(self.id),
            "chunk_id": str(self.chunk_id),
            "model_name": self.model_name,
            "model_version": self.model_version,
            "dimensions": self.dimensions,
            "generation_time_ms": self.generation_time_ms,
            "cached": self.cached,
            "created_at": self.created_at.isoformat()
        }
