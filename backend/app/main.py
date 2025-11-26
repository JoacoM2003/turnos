from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.infrastructure.db.base import Base
from app.infrastructure.db.database import engine

# Importar todos los modelos
from app.infrastructure.db import models

# Importar routers
from app.api.v1.routers.horario_router import router as horario_router
from app.api.v1.routers.auth_router import router as auth_router
from app.api.v1.routers.servicio_router import router as servicio_router
from app.api.v1.routers.recurso_router import router as recurso_router
from app.api.v1.routers.reserva_router import router as reserva_router

app = FastAPI(
    title=settings.project_name,
    description="API para gestión de reservas de instalaciones",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router, prefix=settings.api_v1)
app.include_router(servicio_router, prefix=settings.api_v1)
app.include_router(recurso_router, prefix=settings.api_v1)
app.include_router(reserva_router, prefix=settings.api_v1)
app.include_router(horario_router, prefix=settings.api_v1)


@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada")


@app.get("/")
def root():
    return {
        "message": "API de Reservas - Sistema de Gestión",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}