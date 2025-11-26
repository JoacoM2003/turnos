from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class BloqueoModel(Base):
    """
    Bloqueos de horarios (vacaciones, días no laborables, etc.)
    """
    __tablename__ = 'bloqueos'
    
    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id', ondelete='CASCADE'), nullable=False, index=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    motivo = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    proveedor = relationship("ProveedorModel", back_populates="bloqueos")