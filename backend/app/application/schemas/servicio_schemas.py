from pydantic import BaseModel, Field
from typing import Optional, List
from app.application.schemas.recurso_schemas import RecursoResponse  # IMPORTAR AQUÍ


class ServicioCreateSchema(BaseModel):
    """Schema para crear un servicio"""
    nombre: str = Field(..., min_length=3, max_length=200)
    descripcion: Optional[str] = None
    categoria: Optional[str] = Field(None, max_length=100)


class ServicioUpdateSchema(BaseModel):
    """Schema para actualizar un servicio"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = None
    categoria: Optional[str] = Field(None, max_length=100)


class ServicioResponse(BaseModel):
    """Schema de respuesta de servicio"""
    id: int
    proveedor_id: int
    nombre: str
    descripcion: Optional[str]
    categoria: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class ServicioWithRecursosResponse(BaseModel):
    """Servicio con sus recursos - SIN HERENCIA"""
    id: int
    proveedor_id: int
    nombre: str
    descripcion: Optional[str]
    categoria: Optional[str]
    is_active: bool
    recursos_count: int
    recursos: List[RecursoResponse]  # AHORA RecursoResponse YA ESTÁ DEFINIDO

    class Config:
        from_attributes = True
