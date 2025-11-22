from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from datetime import datetime
from app.infraestructure.db.base import Base

class TurnoModel(Base):
    __tablename__ = 'turnos'
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    servicio_id = Column(Integer, ForeignKey('servicios.id'), nullable=False)
    estado = Column(String, nullable=False, default='pendiente')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
