from sqlalchemy import Column, Integer, Time, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class HorarioDisponibleModel(Base):
    """
    Horarios y precios de disponibilidad de un recurso
    Ejemplo: Cancha 1 - Lunes 10:00-11:00 = $5000
    """
    __tablename__ = 'horarios_disponibles'
    
    id = Column(Integer, primary_key=True, index=True)
    recurso_id = Column(Integer, ForeignKey('recursos.id', ondelete='CASCADE'), nullable=False, index=True)
    
    dia_semana = Column(Integer, nullable=False)  # 0=Lunes, 6=Domingo
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    
    # Precio por esta franja horaria
    precio = Column(Float, nullable=False)
    
    # Duración del slot en minutos (ej: 60 min)
    duracion_minutos = Column(Integer, nullable=False, default=60)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    recurso = relationship("RecursoModel", back_populates="horarios_disponibles")
