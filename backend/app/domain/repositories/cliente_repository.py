from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.cliente import Cliente


class ClienteRepository(ABC):
    """
    Interface del repositorio de clientes
    """

    @abstractmethod
    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por el ID de usuario"""
        pass

    @abstractmethod
    def list(self) -> List[Cliente]:
        """Lista todos los clientes"""
        pass

    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente:
        """Guarda o actualiza un cliente"""
        pass

    @abstractmethod
    def delete(self, cliente_id: int) -> None:
        """Elimina un cliente"""
        pass
