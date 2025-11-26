from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class ProveedorModel(Base):
    """
    Perfil de Proveedor - Extiende la información del usuario
    """
    __tablename__ = 'proveedores'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    especialidad = Column(String(100), nullable=False)
    matricula = Column(String(50), unique=True, nullable=True, index=True)
    telefono = Column(String(20), nullable=True)
    biografia = Column(Text, nullable=True)
    foto_url = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    user = relationship("UserModel", back_populates="proveedor")
    servicios = relationship("ServicioModel", back_populates="proveedor", cascade="all, delete-orphan")
    horarios = relationship("HorarioModel", back_populates="proveedor", cascade="all, delete-orphan")
    bloqueos = relationship("BloqueoModel", back_populates="proveedor", cascade="all, delete-orphan")
    