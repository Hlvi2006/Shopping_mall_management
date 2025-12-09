from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Abstract Base Class (Mücərrəd Əsas Sinif).
    OOP Principles: Abstraction, Inheritance.
    Bütün modellər bu sinifdən törəməlidir.
    """

    @abstractmethod
    def to_dict(self):
        """Obyekti lüğətə (dictionary) çevirən metod. Mütləq yazılmalıdır."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """Lüğətdən obyekt yaradan metod. Mütləq yazılmalıdır."""
        pass
    
    def __repr__(self):
        """Debug zamanı obyekti təmiz göstərmək üçün."""
        return f"<{self.__class__.__name__} Object>"