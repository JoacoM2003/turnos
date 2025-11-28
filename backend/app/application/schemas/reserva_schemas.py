from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone, time
from typing import Optional


class ReservaCreateSchema(BaseModel):
    """Schema para crear una reserva"""
    recurso_id: int = Field(..., gt=0)
    fecha_hora_inicio: datetime
    duracion_minutos: int = Field(..., gt=0)
    notas_cliente: Optional[str] = None
    
    @field_validator('fecha_hora_inicio')
    @classmethod
    def validate_fecha_futura(cls, v: datetime) -> datetime:
        """Valida que la fecha sea futura"""
        # Hacer ambos datetime conscientes de zona horaria (aware)
        now = datetime.now(timezone.utc)
        
        # Si v no tiene timezone, asumimos UTC
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        
        if v <= now:
            raise ValueError('La fecha de reserva debe ser futura')
        
        return v


class ReservaResponse(BaseModel):
    """Schema de respuesta de reserva"""
    id: int
    cliente_id: int
    recurso_id: int
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    duracion_minutos: int
    estado: str
    precio_total: float
    seña: Optional[float]
    saldo_pendiente: Optional[float]
    pago_completo: bool
    notas_cliente: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ReservaDetailResponse(BaseModel):
    """Reserva con información completa (para mostrar al usuario)"""
    # Datos de la reserva
    id: int
    cliente_id: int
    recurso_id: int
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    duracion_minutos: int
    estado: str
    precio_total: float
    seña: Optional[float]
    saldo_pendiente: Optional[float]
    pago_completo: bool
    notas_cliente: Optional[str]
    created_at: datetime
    
    # Datos relacionados (nombres legibles)
    recurso_nombre: str
    servicio_nombre: str
    cliente_nombre: str

    class Config:
        from_attributes = True


class PagoReservaSchema(BaseModel):
    """Schema para registrar un pago"""
    monto: float = Field(..., gt=0, description="Monto a pagar")
    metodo_pago: str = Field(
        ..., 
        pattern="^(efectivo|tarjeta|transferencia)$",
        description="Método de pago: efectivo, tarjeta o transferencia"
    )
    es_pago_completo: bool = Field(
        default=False,
        description="True si es el pago completo, False si es seña/adelanto"
    )


class CancelarReservaSchema(BaseModel):
    """Schema para cancelar una reserva"""
    motivo: Optional[str] = Field(
        None, 
        max_length=500,
        description="Motivo de la cancelación (opcional)"
    )


class DisponibilidadQuerySchema(BaseModel):
    """Schema para consultar disponibilidad"""
    recurso_id: int = Field(..., gt=0)
    fecha: str = Field(..., description="Fecha en formato YYYY-MM-DD")


class DisponibilidadSlotResponse(BaseModel):
    """Schema para un slot de disponibilidad"""
    hora_inicio: time
    hora_fin: time
    precio: float
    disponible: bool
    reserva_id: Optional[int] = None  # Si está ocupado, ID de la reserva

    class Config:
        from_attributes = True