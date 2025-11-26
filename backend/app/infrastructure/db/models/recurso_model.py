from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class RecursoModel(Base):
    """
    Recurso/Instalación específica (Ej: Cancha 1, Cancha 2, Sala A)
    """
    __tablename__ = 'recursos'
    
    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey('servicios.id', ondelete='CASCADE'), nullable=False, index=True)
    
    nombre = Column(String(200), nullable=False)  # "Cancha 1", "Cancha Principal"
    descripcion = Column(Text, nullable=True)  # "Césped sintético, iluminación LED"
    capacidad = Column(Integer, nullable=True)  # Cantidad de personas
    
    # Foto/imagen del recurso
    imagen_url = Column(String(500), nullable=True)
    
    # Características adicionales (JSON o campos específicos)
    caracteristicas = Column(Text, nullable=True)  # "techada, vestuarios, estacionamiento"
    
    is_active = Column(Boolean, default=True)
    orden = Column(Integer, default=0)  # Para ordenar en listados
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    servicio = relationship("ServicioModel", back_populates="recursos")
    horarios_disponibles = relationship("HorarioDisponibleModel", back_populates="recurso", cascade="all, delete-orphan")
    reservas = relationship("ReservaModel", back_populates="recurso")
    bloqueos = relationship("BloqueoRecursoModel", back_populates="recurso", cascade="all, delete-orphan")
