from app.domain.entities.turno import Turno
from app.domain.interfaces.turno_interface import TurnoRepositoryInterface
from app.infraestructure.db.models.turno_model import TurnoModel
from app.infraestructure.db.mappers.turno_mapper import TurnoMapper
from sqlalchemy.orm import Session

class TurnoRepository(TurnoRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def crear_turno(self, turno: Turno) -> Turno:
        model = TurnoMapper.to_model(turno)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return TurnoMapper.to_entity(model)

    def obtener_turno(self, turno_id: int) -> Turno:
        model = self.session.query(TurnoModel).filter_by(id=turno_id).first()
        if not model:
            raise ValueError('Turno no encontrado')
        return TurnoMapper.to_entity(model)
