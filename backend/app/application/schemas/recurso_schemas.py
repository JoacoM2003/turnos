from pydantic import BaseModel, Field
from typing import Optional


class RecursoCreateSchema(BaseModel):
    """Schema para crear un recurso"""
    servicio_id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=200)
    descripcion: Optional[str] = None
    capacidad: Optional[int] = Field(None, gt=0)
    caracteristicas: Optional[str] = None


class RecursoUpdateSchema(BaseModel):
    """Schema para actualizar un recurso"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=200)
    descripcion: Optional[str] = None
    capacidad: Optional[int] = Field(None, gt=0)
    caracteristicas: Optional[str] = None
    orden: Optional[int] = None


class RecursoResponse(BaseModel):
    """Schema de respuesta de recurso"""
    id: int
    servicio_id: int
    nombre: str
    descripcion: Optional[str]
    capacidad: Optional[int]
    imagen_url: Optional[str]
    caracteristicas: Optional[str]
    is_active: bool
    orden: int

    class Config:
        from_attributes = True
