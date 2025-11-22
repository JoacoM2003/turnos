from dataclasses import dataclass
from app.domain.entities.turno import Turno
from app.domain.value_objects.turno_fecha import TurnoFecha
from app.domain.interfaces.turno_interface import TurnoRepositoryInterface

@dataclass
class CreateTurnoDTO:
    fecha: str
    cliente_id: int
    servicio_id: int

class CrearTurnoUseCase:
    def __init__(self, turno_repo: TurnoRepositoryInterface):
        self.turno_repo = turno_repo

    def execute(self, data: CreateTurnoDTO) -> Turno:
        fecha_vo = TurnoFecha(data.fecha)
        turno = Turno.crear(fecha=fecha_vo, cliente_id=data.cliente_id, servicio_id=data.servicio_id)
        return self.turno_repo.crear_turno(turno)
