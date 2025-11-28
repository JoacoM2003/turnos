# ============================================
# api/v1/routers/recurso_router.py (CORREGIDO - SIN ENDPOINTS DE RESERVA)
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.application.schemas.recurso_schemas import (
    RecursoCreateSchema,
    RecursoUpdateSchema,
    RecursoResponse
)
from app.infrastructure.db.database import get_session
from app.infrastructure.db.models.recurso_model import RecursoModel
from app.infrastructure.db.models.servicio_model import ServicioModel
from app.core.security import get_current_proveedor
from app.domain.entities.user import User

router = APIRouter(prefix='/recursos', tags=['Recursos/Instalaciones'])


@router.post('/', response_model=RecursoResponse, status_code=status.HTTP_201_CREATED)
def crear_recurso(
    data: RecursoCreateSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Crea un nuevo recurso (cancha, sala, etc.) para un servicio
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        servicio = session.query(ServicioModel).filter(
            ServicioModel.id == data.servicio_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado o no te pertenece"
            )
        
        recurso = RecursoModel(
            servicio_id=data.servicio_id,
            nombre=data.nombre,
            descripcion=data.descripcion,
            capacidad=data.capacidad,
            caracteristicas=data.caracteristicas
        )
        
        session.add(recurso)
        session.commit()
        session.refresh(recurso)
        
        return RecursoResponse.model_validate(recurso)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear recurso"
        )


@router.get('/servicio/{servicio_id}', response_model=List[RecursoResponse])
def listar_recursos_por_servicio(
    servicio_id: int,
    session: Session = Depends(get_session)
):
    """
    Lista todos los recursos de un servicio (público para clientes)
    """
    try:
        recursos = session.query(RecursoModel).filter(
            RecursoModel.servicio_id == servicio_id,
            RecursoModel.is_active == True
        ).order_by(RecursoModel.orden).all()
        
        return [RecursoResponse.model_validate(r) for r in recursos]
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar recursos"
        )


@router.get('/{recurso_id}', response_model=RecursoResponse)
def obtener_recurso(
    recurso_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtiene un recurso por ID
    """
    try:
        recurso = session.query(RecursoModel).filter(
            RecursoModel.id == recurso_id
        ).first()
        
        if not recurso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurso no encontrado"
            )
        
        return RecursoResponse.model_validate(recurso)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener recurso"
        )


@router.patch('/{recurso_id}', response_model=RecursoResponse)
def actualizar_recurso(
    recurso_id: int,
    data: RecursoUpdateSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Actualiza un recurso (solo el proveedor dueño)
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        recurso = session.query(RecursoModel).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            RecursoModel.id == recurso_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not recurso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurso no encontrado o no autorizado"
            )
        
        if data.nombre is not None:
            recurso.nombre = data.nombre
        if data.descripcion is not None:
            recurso.descripcion = data.descripcion
        if data.capacidad is not None:
            recurso.capacidad = data.capacidad
        if data.caracteristicas is not None:
            recurso.caracteristicas = data.caracteristicas
        if data.orden is not None:
            recurso.orden = data.orden
        
        from datetime import datetime
        recurso.updated_at = datetime.utcnow()
        
        session.commit()
        session.refresh(recurso)
        
        return RecursoResponse.model_validate(recurso)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar recurso"
        )


@router.delete('/{recurso_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_recurso(
    recurso_id: int,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Desactiva un recurso (soft delete)
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        recurso = session.query(RecursoModel).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            RecursoModel.id == recurso_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not recurso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recurso no encontrado o no autorizado"
            )
        
        recurso.is_active = False
        session.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar recurso"
        )