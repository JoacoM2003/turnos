from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.servicio import Servicio


class ServicioRepository(ABC):
    """
    Interface del repositorio de servicios
    """

    @abstractmethod
    def save(self, servicio: Servicio) -> Servicio:
        pass

    @abstractmethod
    def get_by_id(self, servicio_id: int) -> Optional[Servicio]:
        pass

    @abstractmethod
    def list_by_proveedor(self, proveedor_id: int) -> List[Servicio]:
        pass

    @abstractmethod
    def search(self, nombre: Optional[str] = None, categoria: Optional[str] = None) -> List[Servicio]:
        pass

    @abstractmethod
    def delete(self, servicio_id: int) -> None:
        pass
