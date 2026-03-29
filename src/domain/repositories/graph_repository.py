"""Graph Repository Interface - Abstract repository for knowledge graph operations."""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID

from ..entities.graph_entity import GraphEntity
from ..entities.graph_relationship import GraphRelationship
from ..entities.graph_community import GraphCommunity


class GraphRepository(ABC):
    """
    Abstract repository for knowledge graph storage and querying.
    Handles entity, relationship, and community persistence.
    """

    @abstractmethod
    async def save_entity(self, entity: GraphEntity) -> GraphEntity:
        """Persist a single entity."""

    @abstractmethod
    async def save_entities(self, entities: List[GraphEntity]) -> List[GraphEntity]:
        """Persist multiple entities."""

    @abstractmethod
    async def get_entity_by_id(self, entity_id: UUID) -> Optional[GraphEntity]:
        """Retrieve entity by ID."""

    @abstractmethod
    async def get_entity_by_name(self, name: str, entity_type: Optional[str] = None) -> Optional[GraphEntity]:
        """Retrieve entity by canonical name, optionally filtered by type."""

    @abstractmethod
    async def search_entities(self, query: str, top_k: int = 10) -> List[GraphEntity]:
        """Search entities by name/description similarity."""

    @abstractmethod
    async def save_relationship(self, relationship: GraphRelationship) -> GraphRelationship:
        """Persist a single relationship."""

    @abstractmethod
    async def save_relationships(self, relationships: List[GraphRelationship]) -> List[GraphRelationship]:
        """Persist multiple relationships."""

    @abstractmethod
    async def get_relationships_for_entity(self, entity_id: UUID) -> List[GraphRelationship]:
        """Get all relationships where entity is source or target."""

    @abstractmethod
    async def get_neighbors(self, entity_id: UUID, max_depth: int = 1) -> Tuple[List[GraphEntity], List[GraphRelationship]]:
        """Get neighboring entities and their connecting relationships up to max_depth hops."""

    @abstractmethod
    async def save_community(self, community: GraphCommunity) -> GraphCommunity:
        """Persist a single community."""

    @abstractmethod
    async def save_communities(self, communities: List[GraphCommunity]) -> List[GraphCommunity]:
        """Persist multiple communities."""

    @abstractmethod
    async def get_community_by_id(self, community_id: UUID) -> Optional[GraphCommunity]:
        """Retrieve community by ID."""

    @abstractmethod
    async def get_communities_for_entity(self, entity_id: UUID) -> List[GraphCommunity]:
        """Get all communities that contain a given entity."""

    @abstractmethod
    async def get_all_communities(self, level: Optional[int] = None) -> List[GraphCommunity]:
        """Get all communities, optionally filtered by hierarchy level."""

    @abstractmethod
    async def get_entities_for_chunks(self, chunk_ids: List[UUID]) -> List[GraphEntity]:
        """Get all entities extracted from the given chunks."""

    @abstractmethod
    async def clear_document_graph(self, document_id: UUID) -> int:
        """Remove all graph data associated with a document. Returns count of removed entities."""
