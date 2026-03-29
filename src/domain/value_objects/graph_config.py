"""Graph Configuration Value Object."""
from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class GraphSearchMode(Enum):
    """How graph context is used in retrieval."""
    LOCAL = "local"       # Entities + neighbors around query-relevant nodes
    GLOBAL = "global"     # Community summaries for broad questions
    HYBRID = "hybrid"     # Combine local entity context + global community summaries


@dataclass(frozen=True)
class GraphConfig:
    """
    Immutable configuration for Graph RAG operations.
    Controls entity extraction and graph search behavior.
    """

    max_entities_per_chunk: int = 10
    max_relationships_per_chunk: int = 15
    entity_types: tuple = (
        "PERSON", "ORGANIZATION", "LOCATION", "CONCEPT",
        "TECHNOLOGY", "EVENT", "PRODUCT", "DOCUMENT"
    )

    community_algorithm: str = "leiden"  # leiden or louvain
    community_resolution: float = 1.0   # higher = more granular communities
    min_community_size: int = 3

    search_mode: GraphSearchMode = GraphSearchMode.LOCAL
    max_graph_depth: int = 2
    max_community_summaries: int = 3
    max_entity_context: int = 10

    # Weighting when combined with vector search
    graph_weight: float = 0.3  # in hybrid vector+graph search

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "max_entities_per_chunk": self.max_entities_per_chunk,
            "max_relationships_per_chunk": self.max_relationships_per_chunk,
            "entity_types": list(self.entity_types),
            "community_algorithm": self.community_algorithm,
            "community_resolution": self.community_resolution,
            "min_community_size": self.min_community_size,
            "search_mode": self.search_mode.value,
            "max_graph_depth": self.max_graph_depth,
            "max_community_summaries": self.max_community_summaries,
            "max_entity_context": self.max_entity_context,
            "graph_weight": self.graph_weight,
        }

    @classmethod
    def for_precise(cls) -> "GraphConfig":
        """Config optimized for precise, entity-focused answers."""
        return cls(
            search_mode=GraphSearchMode.LOCAL,
            max_graph_depth=1,
            max_entity_context=5,
            graph_weight=0.4,
        )

    @classmethod
    def for_broad(cls) -> "GraphConfig":
        """Config optimized for broad, thematic questions."""
        return cls(
            search_mode=GraphSearchMode.GLOBAL,
            max_community_summaries=5,
            graph_weight=0.5,
        )
