from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.value_objects.turno_fecha import TurnoFecha

@dataclass
class Turno:
    id: Optional[int]
    fecha: TurnoFecha
    cliente_id: int
    servicio_id: int
    estado: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def crear(cls, fecha: TurnoFecha, cliente_id: int, servicio_id: int):
        now = datetime.now()
        return cls(id=None, fecha=fecha, cliente_id=cliente_id, servicio_id=servicio_id, estado="pendiente", created_at=now, updated_at=now)

    def cancelar(self):
        if self.estado == "cancelado":
            raise ValueError("El turno ya está cancelado")
        self.estado = "cancelado"
        self.updated_at = datetime.now()

    def reprogramar(self, nueva_fecha: TurnoFecha):
        if self.estado == "cancelado":
            raise ValueError("No se puede reprogramar un turno cancelado")
        self.fecha = nueva_fecha
        self.updated_at = datetime.now()
