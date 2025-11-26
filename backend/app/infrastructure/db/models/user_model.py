from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class UserModel(Base):
    """
    Usuario del sistema - Tabla de autenticación
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default='cliente')  # cliente, proveedor, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones 1:1
    cliente = relationship(
        "ClienteModel", 
        back_populates="user", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    proveedor = relationship(
        "ProveedorModel", 
        back_populates="user", 
        uselist=False,
        cascade="all, delete-orphan"
    )