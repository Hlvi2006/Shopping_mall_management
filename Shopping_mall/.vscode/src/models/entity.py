from abc import ABC, abstractmethod

class Entity(ABC):
    """Abstract base class for entities, demonstrating abstraction."""
    @abstractmethod
    def to_dict(self):
        pass