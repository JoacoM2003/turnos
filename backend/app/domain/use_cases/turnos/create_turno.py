from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.entities.turno import Turno
from app.domain.value_objects.turno_fecha import TurnoFecha
from app.domain.repositories.turno_repository import TurnoRepository


@dataclass
class CreateTurnoDTO:
    cliente_id: int
    proveedor_id: int
    servicio_id: int
    fecha_hora: datetime
    duracion_minutos: int
    precio: float
    notas_cliente: Optional[str] = None


class CreateTurnoUseCase:
    """
    Caso de uso: Crear un nuevo turno
    """

    def __init__(self, turno_repository: TurnoRepository):
        self.turno_repository = turno_repository

    def execute(self, data: CreateTurnoDTO) -> Turno:
        # 1) Crear value object de fecha (valida que sea futura)
        fecha_vo = TurnoFecha(data.fecha_hora)

        # 2) Crear entidad usando factory method
        turno = Turno.crear(
            cliente_id=data.cliente_id,
            proveedor_id=data.proveedor_id,
            servicio_id=data.servicio_id,
            fecha_hora=fecha_vo,
            duracion_minutos=data.duracion_minutos,
            precio=data.precio,
            notas_cliente=data.notas_cliente
        )

        # 3) Persistir
        saved_turno = self.turno_repository.save(turno)

        return saved_turno