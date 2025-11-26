from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Cliente:
    id: Optional[int]
    user_id: int
    nombre: str
    apellido: str
    telefono: Optional[str]
    dni: Optional[str]
    fecha_nacimiento: Optional[datetime]
    direccion: Optional[str]
    notas: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        user_id: int,
        nombre: str,
        apellido: str,
        telefono: Optional[str] = None,
        dni: Optional[str] = None,
        fecha_nacimiento: Optional[datetime] = None,
        direccion: Optional[str] = None,
        notas: Optional[str] = None,
    ):
        now = datetime.now(timezone.utc)
        return cls(
            id=None,
            user_id=user_id,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
            direccion=direccion,
            notas=notas,
            created_at=now,
            updated_at=now,
        )

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"