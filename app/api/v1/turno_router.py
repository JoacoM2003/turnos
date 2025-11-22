from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas.turno import TurnoCreateSchema, TurnoSchema
from app.domain.use_cases.turnos.create_turno import CrearTurnoUseCase, CreateTurnoDTO
from app.infraestructure.repositories.turno_repository import TurnoRepository
from app.infraestructure.db.base import Base
from app.infraestructure.db.models.turno_model import TurnoModel
from app.infraestructure.db.database import get_session # Dependencia real DB

router = APIRouter(prefix='/turnos', tags=['Turnos'])

@router.post('/', response_model=TurnoSchema)
def crear_turno(turno: TurnoCreateSchema, session: Session = Depends(get_session)):
    repo = TurnoRepository(session)
    use_case = CrearTurnoUseCase(repo)
    try:
        turno_dto = CreateTurnoDTO(
            fecha=turno.fecha,
            cliente_id=turno.cliente_id,
            servicio_id=turno.servicio_id,
        )
        entidad = use_case.execute(turno_dto)
        return {
            "id": entidad.id,
            "fecha": entidad.fecha.value,
            "cliente_id": entidad.cliente_id,
            "servicio_id": entidad.servicio_id,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
