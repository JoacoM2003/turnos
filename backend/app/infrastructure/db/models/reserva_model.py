from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.db.base import Base


class ReservaModel(Base):
    """
    Reserva de un recurso específico
    """
    __tablename__ = 'reservas'
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)
    recurso_id = Column(Integer, ForeignKey('recursos.id', ondelete='RESTRICT'), nullable=False, index=True)
    
    # Fecha y hora de la reserva
    fecha_hora_inicio = Column(DateTime, nullable=False, index=True)
    fecha_hora_fin = Column(DateTime, nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    
    # Estado de la reserva
    estado = Column(String(50), nullable=False, default='pendiente', index=True)
    # Estados: pendiente, confirmada, cancelada, completada, no_asistio
    
    # Información de pago
    precio_total = Column(Float, nullable=False)
    seña = Column(Float, nullable=True)  # Seña/Adelanto pagado
    saldo_pendiente = Column(Float, nullable=True)
    metodo_pago = Column(String(50), nullable=True)  # efectivo, tarjeta, transferencia
    pago_completo = Column(Boolean, default=False)
    pago_confirmado = Column(Boolean, default=False)
    notas_pago = Column(Text, nullable=True)
    
    # Notas
    notas_cliente = Column(Text, nullable=True)
    notas_internas = Column(Text, nullable=True)  # Solo visible para el proveedor
    
    # Cancelación
    motivo_cancelacion = Column(String(500), nullable=True)
    fecha_cancelacion = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    cliente = relationship("ClienteModel", back_populates="reservas")
    recurso = relationship("RecursoModel", back_populates="reservas")

