from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Proveedor:
    id: Optional[int]
    user_id: int
    nombre: str
    apellido: str
    especialidad: str
    matricula: Optional[str]
    telefono: Optional[str]
    biografia: Optional[str]
    foto_url: Optional[str]
    is_available: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        user_id: int,
        nombre: str,
        apellido: str,
        especialidad: str,
        matricula: Optional[str] = None,
        telefono: Optional[str] = None,
        biografia: Optional[str] = None,
    ):
        now = datetime.now(timezone.utc)
        return cls(
            id=None,
            user_id=user_id,
            nombre=nombre,
            apellido=apellido,
            especialidad=especialidad,
            matricula=matricula,
            telefono=telefono,
            biografia=biografia,
            foto_url=None,
            is_available=True,
            created_at=now,
            updated_at=now,
        )

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def activar(self):
        self.is_available = True
        self.updated_at = datetime.now(timezone.utc)

    def desactivar(self):
        self.is_available = False
        self.updated_at = datetime.now(timezone.utc)