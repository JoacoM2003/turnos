from app.domain.entities.turno import Turno
from app.domain.value_objects.turno_fecha import TurnoFecha
from app.infraestructure.db.models.turno_model import TurnoModel

class TurnoMapper:
    @staticmethod
    def to_entity(model: TurnoModel) -> Turno:
        return Turno(
            id=model.id,
            fecha=TurnoFecha(model.fecha),
            cliente_id=model.cliente_id,
            servicio_id=model.servicio_id,
            estado=model.estado,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    @staticmethod
    def to_model(entity: Turno) -> TurnoModel:
        model = TurnoModel(
            id=entity.id,
            fecha=entity.fecha.value,
            cliente_id=entity.cliente_id,
            servicio_id=entity.servicio_id,
            estado=entity.estado,
        )
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        return model
