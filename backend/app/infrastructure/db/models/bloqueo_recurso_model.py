from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class BloqueoRecursoModel(Base):
    """
    Bloqueos de un recurso específico (mantenimiento, reservas privadas)
    """
    __tablename__ = 'bloqueos_recursos'
    
    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey('recursos.id', ondelete='CASCADE'), nullable=False, index=True)
    
    fecha_hora_inicio = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=False)
    motivo = Column(Text, nullable=True)
    tipo = Column(String(50), default='mantenimiento')  # mantenimiento, evento_privado, clausura
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    recurso = relationship("RecursoModel", back_populates="bloqueos")
