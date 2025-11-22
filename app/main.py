from fastapi import FastAPI
from app.api.v1.turno_router import router as turno_router
from app.infraestructure.db.base import Base
from app.infraestructure.db.database import engine
from app.infraestructure.db.models.user_model import UserModel
from app.infraestructure.db.models.turno_model import TurnoModel
from app.infraestructure.db.models.cliente_model import ClienteModel
from app.infraestructure.db.models.servicio_model import ServicioModel

app = FastAPI()
app.include_router(turno_router)

# Crea las tablas (para pruebas rápidas mientras desarrollas)
Base.metadata.create_all(bind=engine)
