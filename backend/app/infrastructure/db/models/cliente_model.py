from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class ClienteModel(Base):
    """
    Perfil de Cliente
    """
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    dni = Column(String(20), unique=True, nullable=True, index=True)
    fecha_nacimiento = Column(Date, nullable=True)
    direccion = Column(String(255), nullable=True)
    notas = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    user = relationship("UserModel", back_populates="cliente")
    reservas = relationship("ReservaModel", back_populates="cliente", cascade="all, delete-orphan")  # CAMBIADO
