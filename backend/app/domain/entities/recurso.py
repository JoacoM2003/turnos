from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Recurso:
    """
    Recurso específico (Cancha, Sala, etc.)
    """
    id: Optional[int]
    servicio_id: int
    nombre: str
    descripcion: Optional[str]
    capacidad: Optional[int]
    imagen_url: Optional[str]
    caracteristicas: Optional[str]
    is_active: bool
    orden: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        servicio_id: int,
        nombre: str,
        descripcion: Optional[str] = None,
        capacidad: Optional[int] = None,
        caracteristicas: Optional[str] = None,
    ):
        now = datetime.now(timezone.utc)
        return cls(
            id=None,
            servicio_id=servicio_id,
            nombre=nombre,
            descripcion=descripcion,
            capacidad=capacidad,
            imagen_url=None,
            caracteristicas=caracteristicas,
            is_active=True,
            orden=0,
            created_at=now,
            updated_at=now,
        )

    def desactivar(self):
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)