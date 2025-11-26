from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.recurso import Recurso


class RecursoRepository(ABC):
    """
    Interface del repositorio de recursos
    """

    @abstractmethod
    def save(self, recurso: Recurso) -> Recurso:
        pass

    @abstractmethod
    def get_by_id(self, recurso_id: int) -> Optional[Recurso]:
        pass

    @abstractmethod
    def list_by_servicio(self, servicio_id: int) -> List[Recurso]:
        pass

    @abstractmethod
    def delete(self, recurso_id: int) -> None:
        pass
