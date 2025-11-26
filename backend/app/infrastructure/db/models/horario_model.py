from sqlalchemy import Column, Integer, Time, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class HorarioModel(Base):
    """
    Horarios de disponibilidad de un proveedor
    """
    __tablename__ = 'horarios'
    
    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id', ondelete='CASCADE'), nullable=False, index=True)
    dia_semana = Column(Integer, nullable=False)  # 0=Lunes, 6=Domingo
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    proveedor = relationship("ProveedorModel", back_populates="horarios")