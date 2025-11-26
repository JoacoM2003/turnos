from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Servicio:
    """
    Tipo de servicio (Fútbol 5, Tenis, etc.)
    """
    id: Optional[int]
    proveedor_id: int
    nombre: str
    descripcion: Optional[str]
    categoria: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        proveedor_id: int,
        nombre: str,
        descripcion: Optional[str] = None,
        categoria: Optional[str] = None,
    ):
        now = datetime.now(timezone.utc)
        return cls(
            id=None,
            proveedor_id=proveedor_id,
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

    def desactivar(self):
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)