from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class ServicioModel(Base):
    """
    Tipo de servicio ofrecido (Ej: Fútbol 5, Tenis, Paddle)
    """
    __tablename__ = 'servicios'
    
    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id', ondelete='CASCADE'), nullable=False, index=True)
    
    nombre = Column(String(200), nullable=False)  # "Fútbol 5", "Tenis"
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=True, index=True)  # "Deportes", "Salud", "Entretenimiento"
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    proveedor = relationship("ProveedorModel", back_populates="servicios")
    recursos = relationship("RecursoModel", back_populates="servicio", cascade="all, delete-orphan")
