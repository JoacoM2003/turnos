from abc import ABC, abstractmethod
from app.domain.entities.turno import Turno

class TurnoRepositoryInterface(ABC):
    @abstractmethod
    def crear_turno(self, turno: Turno) -> Turno:
        pass

    @abstractmethod
    def obtener_turno(self, turno_id: int) -> Turno:
        pass
