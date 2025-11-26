from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import time

from app.application.schemas.horario_disponible_schemas import (
    HorarioDisponibleCreateSchema,
    HorarioDisponibleBulkCreateSchema,
    HorarioDisponibleResponse
)
from app.infrastructure.db.database import get_session
from app.infrastructure.db.models.horario_disponible_model import HorarioDisponibleModel
from app.infrastructure.db.models.recurso_model import RecursoModel
from app.infrastructure.db.models.servicio_model import ServicioModel
from app.core.security import get_current_proveedor
from app.domain.entities.user import User

router = APIRouter(prefix='/horarios', tags=['Horarios Disponibles'])


@router.post('/', response_model=HorarioDisponibleResponse, status_code=status.HTTP_201_CREATED)
def crear_horario(
    data: HorarioDisponibleCreateSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Crea un horario disponible para un recurso (solo proveedores)
    
    **Días de la semana:**
    - 0 = Lunes
    - 1 = Martes
    - 2 = Miércoles
    - 3 = Jueves
    - 4 = Viernes
    - 5 = Sábado
    - 6 = Domingo
    
    **Ejemplo:**
    Para configurar que una cancha está disponible los lunes de 10:00 a 22:00
    con precio $5000:
    ```json
    {
      "recurso_id": 1,
      "dia_semana": 0,
      "hora_inicio": "10:00:00",
      "hora_fin": "22:00:00",
      "precio": 5000,
      "duracion_minutos": 60
    }
    ```
    """
    try:
        # Verificar que el recurso pertenece al proveedor
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        recurso = session.query(RecursoModel).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            RecursoModel.id == data.recurso_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not recurso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurso no encontrado o no te pertenece"
            )
        
        # Validar que hora_inicio < hora_fin
        if data.hora_inicio >= data.hora_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora de inicio debe ser anterior a la hora de fin"
            )
        
        # Crear horario
        horario = HorarioDisponibleModel(
            recurso_id=data.recurso_id,
            dia_semana=data.dia_semana,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
            precio=data.precio,
            duracion_minutos=data.duracion_minutos
        )
        
        session.add(horario)
        session.commit()
        session.refresh(horario)
        
        return HorarioDisponibleResponse.model_validate(horario)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error al crear horario: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear horario"
        )


@router.post('/bulk', response_model=List[HorarioDisponibleResponse], status_code=status.HTTP_201_CREATED)
def crear_horarios_masivo(
    data: HorarioDisponibleBulkCreateSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Crea múltiples horarios a la vez para varios días
    
    **Útil para configurar toda la semana de una vez**
    
    **Ejemplo:**
    Configurar lunes a viernes (0-4) de 10:00 a 22:00:
    ```json
    {
      "recurso_id": 1,
      "dias_semana": [0, 1, 2, 3, 4],
      "hora_inicio": "10:00:00",
      "hora_fin": "22:00:00",
      "precio": 5000,
      "duracion_minutos": 60
    }
    ```
    """
    try:
        # Verificar que el recurso pertenece al proveedor
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        recurso = session.query(RecursoModel).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            RecursoModel.id == data.recurso_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not recurso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurso no encontrado o no te pertenece"
            )
        
        # Validar días
        if any(dia < 0 or dia > 6 for dia in data.dias_semana):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los días deben estar entre 0 (Lunes) y 6 (Domingo)"
            )
        
        # Validar horas
        if data.hora_inicio >= data.hora_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora de inicio debe ser anterior a la hora de fin"
            )
        
        # Crear horarios para cada día
        horarios_creados = []
        for dia in data.dias_semana:
            horario = HorarioDisponibleModel(
                recurso_id=data.recurso_id,
                dia_semana=dia,
                hora_inicio=data.hora_inicio,
                hora_fin=data.hora_fin,
                precio=data.precio,
                duracion_minutos=data.duracion_minutos
            )
            session.add(horario)
            horarios_creados.append(horario)
        
        session.commit()
        
        for horario in horarios_creados:
            session.refresh(horario)
        
        return [HorarioDisponibleResponse.model_validate(h) for h in horarios_creados]
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error al crear horarios: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear horarios"
        )


@router.get('/recurso/{recurso_id}', response_model=List[HorarioDisponibleResponse])
def listar_horarios_recurso(
    recurso_id: int,
    session: Session = Depends(get_session)
):
    """
    Lista todos los horarios disponibles de un recurso
    
    **Abierto para todos** - Los clientes necesitan ver esto para saber
    qué horarios están disponibles.
    """
    try:
        horarios = session.query(HorarioDisponibleModel).filter(
            HorarioDisponibleModel.recurso_id == recurso_id,
            HorarioDisponibleModel.is_active == True
        ).order_by(
            HorarioDisponibleModel.dia_semana,
            HorarioDisponibleModel.hora_inicio
        ).all()
        
        return [HorarioDisponibleResponse.model_validate(h) for h in horarios]
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar horarios"
        )


@router.delete('/{horario_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_horario(
    horario_id: int,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Desactiva un horario (soft delete)
    
    Solo el proveedor dueño puede eliminar horarios.
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        horario = session.query(HorarioDisponibleModel).join(
            RecursoModel, HorarioDisponibleModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            HorarioDisponibleModel.id == horario_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not horario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Horario no encontrado o no autorizado"
            )
        
        horario.is_active = False
        session.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar horario"
        )

@router.patch('/{horario_id}', response_model=HorarioDisponibleResponse)
def actualizar_horario(
    horario_id: int,
    data: HorarioDisponibleCreateSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Actualiza un horario existente
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        horario = session.query(HorarioDisponibleModel).join(
            RecursoModel, HorarioDisponibleModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            HorarioDisponibleModel.id == horario_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not horario:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        
        horario.dia_semana = data.dia_semana
        horario.hora_inicio = data.hora_inicio
        horario.hora_fin = data.hora_fin
        horario.precio = data.precio
        horario.duracion_minutos = data.duracion_minutos
        
        session.commit()
        session.refresh(horario)
        
        return HorarioDisponibleResponse.model_validate(horario)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar")