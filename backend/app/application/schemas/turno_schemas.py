from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TurnoCreateSchema(BaseModel):
    """Schema para crear un turno"""
    profesional_id: int = Field(..., gt=0)
    servicio_id: int = Field(..., gt=0)
    fecha_hora: datetime
    notas_cliente: Optional[str] = None


class TurnoResponse(BaseModel):
    """Schema de respuesta de turno"""
    id: int
    cliente_id: int
    profesional_id: int
    servicio_id: int
    fecha_hora: datetime
    duracion_minutos: int
    estado: str
    precio: float
    notas_cliente: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TurnoDetailResponse(TurnoResponse):
    """Schema detallado de turno con relaciones"""
    cliente_nombre: str
    profesional_nombre: str
    servicio_nombre: str