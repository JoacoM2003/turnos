from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.domain.entities.reserva import Reserva
from app.domain.repositories.reserva_repository import ReservaRepository
from app.infrastructure.db.models.reserva_model import ReservaModel
from app.infrastructure.db.models.recurso_model import RecursoModel
from app.infrastructure.db.models.servicio_model import ServicioModel
from app.infrastructure.db.mappers.reserva_mapper import ReservaMapper


class SQLAlchemyReservaRepository(ReservaRepository):
    """
    Implementación del repositorio de reservas usando SQLAlchemy
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, reserva: Reserva) -> Reserva:
        if reserva.id is not None:
            # Actualizar
            model = self.session.query(ReservaModel).filter(
                ReservaModel.id == reserva.id
            ).first()
            if not model:
                raise ValueError(f"Reserva with id {reserva.id} not found")
            
            ReservaMapper.update_model_from_entity(model, reserva)
        else:
            # Crear nuevo
            model = ReservaMapper.to_model(reserva)
            self.session.add(model)

        self.session.commit()
        self.session.refresh(model)
        return ReservaMapper.to_entity(model)

    def get_by_id(self, reserva_id: int) -> Optional[Reserva]:
        model = self.session.query(ReservaModel).filter(
            ReservaModel.id == reserva_id
        ).first()
        return ReservaMapper.to_entity(model) if model else None

    def list_by_cliente(self, cliente_id: int) -> List[Reserva]:
        models = self.session.query(ReservaModel).filter(
            ReservaModel.cliente_id == cliente_id
        ).order_by(ReservaModel.fecha_hora_inicio.desc()).all()
        
        return [ReservaMapper.to_entity(m) for m in models]

    def list_by_recurso(self, recurso_id: int, fecha_desde: datetime, fecha_hasta: datetime) -> List[Reserva]:
        models = self.session.query(ReservaModel).filter(
            ReservaModel.recurso_id == recurso_id,
            ReservaModel.fecha_hora_inicio >= fecha_desde,
            ReservaModel.fecha_hora_inicio <= fecha_hasta,
            ReservaModel.estado.in_(['pendiente', 'confirmada'])
        ).order_by(ReservaModel.fecha_hora_inicio).all()
        
        return [ReservaMapper.to_entity(m) for m in models]

    def list_by_proveedor(self, proveedor_id: int, fecha_desde: Optional[datetime] = None) -> List[Reserva]:
        query = self.session.query(ReservaModel).join(
            RecursoModel, ReservaModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            ServicioModel.proveedor_id == proveedor_id
        )
        
        if fecha_desde:
            query = query.filter(ReservaModel.fecha_hora_inicio >= fecha_desde)
        
        models = query.order_by(ReservaModel.fecha_hora_inicio.desc()).all()
        return [ReservaMapper.to_entity(m) for m in models]

    def delete(self, reserva_id: int) -> None:
        model = self.session.query(ReservaModel).filter(
            ReservaModel.id == reserva_id
        ).first()
        if model:
            self.session.delete(model)
            self.session.commit()