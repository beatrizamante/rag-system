"""Document Status Value Object."""
from enum import Enum


class DocumentStatus(Enum):
    """
    Enumeration of document processing states.
    Represents the lifecycle of a document in the system.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    ARCHIVED = "archived"

    @classmethod
    def from_string(cls, value: str) -> "DocumentStatus":
        """Create status from string value."""
        try:
            return cls(value.lower())
        except ValueError:
            return cls.PENDING

    def is_terminal(self) -> bool:
        """Check if status is a terminal state."""
        return self in (self.PROCESSED, self.FAILED, self.ARCHIVED)

    def can_transition_to(self, new_status: "DocumentStatus") -> bool:
        """Check if transition to new status is valid."""
        valid_transitions = {
            self.PENDING: {self.PROCESSING, self.FAILED},
            self.PROCESSING: {self.PROCESSED, self.FAILED},
            self.PROCESSED: {self.ARCHIVED},
            self.FAILED: {self.PENDING},
            self.ARCHIVED: set()
        }
        return new_status in valid_transitions.get(self, set())
