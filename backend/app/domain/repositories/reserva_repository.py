from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

from app.domain.entities.reserva import Reserva


class ReservaRepository(ABC):
    """
    Interface del repositorio de reservas
    """

    @abstractmethod
    def save(self, reserva: Reserva) -> Reserva:
        """Guarda o actualiza una reserva"""
        pass

    @abstractmethod
    def get_by_id(self, reserva_id: int) -> Optional[Reserva]:
        """Obtiene una reserva por su ID"""
        pass

    @abstractmethod
    def list_by_cliente(self, cliente_id: int) -> List[Reserva]:
        """Lista reservas de un cliente"""
        pass

    @abstractmethod
    def list_by_recurso(self, recurso_id: int, fecha_desde: datetime, fecha_hasta: datetime) -> List[Reserva]:
        """Lista reservas de un recurso en un rango de fechas"""
        pass

    @abstractmethod
    def list_by_proveedor(self, proveedor_id: int, fecha_desde: Optional[datetime] = None) -> List[Reserva]:
        """Lista todas las reservas de un proveedor"""
        pass

    @abstractmethod
    def delete(self, reserva_id: int) -> None:
        """Elimina una reserva"""
        pass