from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional


class ReservaCreateSchema(BaseModel):
    """Schema para crear una reserva"""
    recurso_id: int = Field(..., gt=0)
    fecha_hora_inicio: datetime
    duracion_minutos: int = Field(..., gt=0)
    notas_cliente: Optional[str] = None
    # Nuevo: Pago al crear reserva
    seña: Optional[float] = Field(None, ge=0, description="Monto de seña/adelanto")
    metodo_pago: Optional[str] = Field(None, pattern="^(efectivo|tarjeta|transferencia)$")
    
    @field_validator('fecha_hora_inicio')
    @classmethod
    def validate_fecha_futura(cls, v: datetime) -> datetime:
        now = datetime.now(timezone.utc)
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        if v <= now:
            raise ValueError('La fecha de reserva debe ser futura')
        return v


class PagoReservaSchema(BaseModel):
    """Schema para registrar/actualizar un pago"""
    monto: float = Field(..., gt=0)
    metodo_pago: str = Field(..., pattern="^(efectivo|tarjeta|transferencia)$")
    confirmado_por_proveedor: bool = Field(default=False)


class ConfirmarPagoSchema(BaseModel):
    """Schema para que el proveedor confirme un pago"""
    pago_confirmado: bool = Field(...)
    notas_pago: Optional[str] = None


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
    pago_confirmado: bool  # Nuevo
    notas_cliente: Optional[str]
    notas_pago: Optional[str]  # Nuevo
    created_at: datetime

    class Config:
        from_attributes = True


class ReservaDetailResponse(ReservaResponse):
    """Reserva con información completa"""
    recurso_nombre: str
    servicio_nombre: str
    cliente_nombre: str

    class Config:
        from_attributes = True


class CancelarReservaSchema(BaseModel):
    """Schema para cancelar una reserva"""
    motivo: Optional[str] = Field(None, max_length=500)


class MarcarNoAsistioSchema(BaseModel):
    """Schema para marcar que el cliente no asistió"""
    notas: Optional[str] = None