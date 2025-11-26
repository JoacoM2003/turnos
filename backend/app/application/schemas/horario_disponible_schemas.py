from pydantic import BaseModel, Field
from datetime import time
from typing import List


class HorarioDisponibleCreateSchema(BaseModel):
    """Schema para crear horario disponible"""
    recurso_id: int = Field(..., gt=0)
    dia_semana: int = Field(..., ge=0, le=6, description="0=Lunes, 6=Domingo")
    hora_inicio: time
    hora_fin: time
    precio: float = Field(..., gt=0)
    duracion_minutos: int = Field(default=60, gt=0)


class HorarioDisponibleBulkCreateSchema(BaseModel):
    """Schema para crear múltiples horarios a la vez"""
    recurso_id: int = Field(..., gt=0)
    dias_semana: List[int] = Field(..., description="Lista de días (0=Lunes, 6=Domingo)")
    hora_inicio: time
    hora_fin: time
    precio: float = Field(..., gt=0)
    duracion_minutos: int = Field(default=60, gt=0)


class HorarioDisponibleResponse(BaseModel):
    """Schema de respuesta de horario"""
    id: int
    recurso_id: int
    dia_semana: int
    hora_inicio: time
    hora_fin: time
    precio: float
    duracion_minutos: int
    is_active: bool

    class Config:
        from_attributes = True