from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.proveedor import Proveedor


class ProveedorRepository(ABC):
    """
    Interface del repositorio de proveedores
    """

    @abstractmethod
    def get_by_id(self, proveedor_id: int) -> Optional[Proveedor]:
        """Obtiene un proveedor por su ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Proveedor]:
        """Obtiene un proveedor por el ID de usuario"""
        pass

    @abstractmethod
    def list(self, is_available: Optional[bool] = None) -> List[Proveedor]:
        """Lista proveedores, opcionalmente filtrados por disponibilidad"""
        pass

    @abstractmethod
    def list_by_especialidad(self, especialidad: str) -> List[Proveedor]:
        """Lista proveedores por especialidad"""
        pass

    @abstractmethod
    def save(self, proveedor: Proveedor) -> Proveedor:
        """Guarda o actualiza un proveedor"""
        pass

    @abstractmethod
    def delete(self, proveedor_id: int) -> None:
        """Elimina un proveedor"""
        pass