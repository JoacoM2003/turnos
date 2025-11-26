from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import date


# ===== SCHEMAS DE REGISTRO =====

class BaseUserRegisterSchema(BaseModel):
    """Schema base para registro (campos comunes)"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")
    username: str = Field(..., min_length=3, max_length=50)
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)


class ClienteRegisterSchema(BaseUserRegisterSchema):
    """Schema para registro de cliente"""
    dni: Optional[str] = Field(None, max_length=20, description="DNI/Documento de identidad")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    direccion: Optional[str] = Field(None, max_length=255)
    
    @validator('dni')
    def validate_dni(cls, v):
        if v and not v.replace('-', '').replace('.', '').isdigit():
            raise ValueError('DNI debe contener solo números, puntos o guiones')
        return v


class ProveedorRegisterSchema(BaseUserRegisterSchema):
    """Schema para registro de proveedor"""
    especialidad: str = Field(..., min_length=3, max_length=100, description="Ej: Peluquería, Masajes")
    matricula: Optional[str] = Field(None, max_length=50, description="Matrícula profesional")
    biografia: Optional[str] = Field(None, max_length=1000, description="Descripción profesional")


# ===== SCHEMAS DE ACTUALIZACIÓN DE PERFIL =====

class ClienteUpdateSchema(BaseModel):
    """Schema para actualizar perfil de cliente"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    dni: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = Field(None, max_length=255)


class ProveedorUpdateSchema(BaseModel):
    """Schema para actualizar perfil de proveedor"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    especialidad: Optional[str] = Field(None, min_length=3, max_length=100)
    matricula: Optional[str] = Field(None, max_length=50)
    biografia: Optional[str] = Field(None, max_length=1000)


# ===== SCHEMAS DE LOGIN =====

class UserLoginSchema(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str


# ===== SCHEMAS DE RESPUESTA =====

class UserResponse(BaseModel):
    """Schema de respuesta básica de usuario"""
    id: int
    email: str
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class ClienteProfileResponse(BaseModel):
    """Schema de perfil completo de cliente"""
    # Datos de usuario
    id: int
    email: str
    username: str
    role: str
    is_active: bool
    
    # Datos de cliente
    cliente_id: int
    nombre: str
    apellido: str
    telefono: Optional[str]
    dni: Optional[str]
    fecha_nacimiento: Optional[date]
    direccion: Optional[str]

    class Config:
        from_attributes = True


class ProveedorProfileResponse(BaseModel):
    """Schema de perfil completo de proveedor"""
    # Datos de usuario
    id: int
    email: str
    username: str
    role: str
    is_active: bool
    
    # Datos de proveedor
    proveedor_id: int
    nombre: str
    apellido: str
    telefono: Optional[str]
    especialidad: str
    matricula: Optional[str]
    biografia: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema de respuesta del token"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
