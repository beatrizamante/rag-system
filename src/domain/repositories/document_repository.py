"""Document Repository Interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.document import Document
from ..value_objects.document_status import DocumentStatus


class DocumentRepository(ABC):
    """
    Abstract repository for document persistence.
    Infrastructure layer must implement this interface.
    """

    @abstractmethod
    async def save(self, document: Document) -> Document:
        """Persist a document."""

    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> Optional[Document]:
        """Retrieve document by ID."""

    @abstractmethod
    async def get_by_filename(self, filename: str) -> Optional[Document]:
        """Retrieve document by filename."""

    @abstractmethod
    async def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[DocumentStatus] = None
    ) -> List[Document]:
        """List documents with pagination and optional status filter."""

    @abstractmethod
    async def update(self, document: Document) -> Document:
        """Update an existing document."""

    @abstractmethod
    async def delete(self, document_id: UUID) -> bool:
        """Delete a document by ID."""

    @abstractmethod
    async def count(self, status: Optional[DocumentStatus] = None) -> int:
        """Count documents, optionally filtered by status."""

    @abstractmethod
    async def get_pending(self, limit: int = 10) -> List[Document]:
        """Get pending documents for processing."""
