from pydantic import BaseModel
from datetime import datetime

class TurnoCreateSchema(BaseModel):
    fecha: datetime
    cliente_id: int
    servicio_id: int

class TurnoSchema(TurnoCreateSchema):
    id: int

    class Config:
        orm_mode = True
