from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.application.schemas.servicio_schemas import (
    ServicioCreateSchema,
    ServicioUpdateSchema,
    ServicioResponse,
    ServicioWithRecursosResponse
)
from app.application.schemas.recurso_schemas import RecursoResponse
from app.infrastructure.db.database import get_session
from app.infrastructure.db.models.servicio_model import ServicioModel
from app.infrastructure.db.models.recurso_model import RecursoModel
from app.core.security import get_current_proveedor
from app.domain.entities.user import User

router = APIRouter(prefix='/servicios', tags=['Servicios'])


@router.post('/', response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def crear_servicio(
    data: ServicioCreateSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Crea un nuevo tipo de servicio (solo proveedores)
    Ejemplo: "Fútbol 5", "Tenis", "Paddle"
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de proveedor no encontrado"
            )
        
        servicio = ServicioModel(
            proveedor_id=proveedor.id,
            nombre=data.nombre,
            descripcion=data.descripcion,
            categoria=data.categoria
        )
        
        session.add(servicio)
        session.commit()
        session.refresh(servicio)
        
        return ServicioResponse.model_validate(servicio)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error al crear servicio: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear servicio"
        )


@router.get('/mis-servicios', response_model=List[ServicioWithRecursosResponse])
def listar_mis_servicios(
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Lista los servicios del proveedor autenticado con sus recursos
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de proveedor no encontrado"
            )
        
        servicios = session.query(ServicioModel).filter(
            ServicioModel.proveedor_id == proveedor.id
        ).all()
        
        resultado = []
        for servicio in servicios:
            recursos = session.query(RecursoModel).filter(
                RecursoModel.servicio_id == servicio.id
            ).all()
            
            # Construir manualmente el response
            resultado.append(ServicioWithRecursosResponse(
                id=servicio.id,
                proveedor_id=servicio.proveedor_id,
                nombre=servicio.nombre,
                descripcion=servicio.descripcion,
                categoria=servicio.categoria,
                is_active=servicio.is_active,
                recursos_count=len(recursos),
                recursos=[RecursoResponse.model_validate(r) for r in recursos]
            ))
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar servicios"
        )


@router.get('/buscar', response_model=List[ServicioResponse])
def buscar_servicios(
    nombre: str = None,
    categoria: str = None,
    session: Session = Depends(get_session)
):
    """
    Busca servicios disponibles (para clientes)
    """
    try:
        query = session.query(ServicioModel).filter(ServicioModel.is_active == True)
        
        if nombre:
            query = query.filter(ServicioModel.nombre.ilike(f'%{nombre}%'))
        
        if categoria:
            query = query.filter(ServicioModel.categoria == categoria)
        
        servicios = query.all()
        
        return [ServicioResponse.model_validate(s) for s in servicios]
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al buscar servicios"
        )


@router.get('/{servicio_id}', response_model=ServicioResponse)
def obtener_servicio(
    servicio_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtiene un servicio por ID
    """
    try:
        servicio = session.query(ServicioModel).filter(
            ServicioModel.id == servicio_id
        ).first()
        
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado"
            )
        
        return ServicioResponse.model_validate(servicio)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener servicio"
        )


@router.patch('/{servicio_id}', response_model=ServicioResponse)
def actualizar_servicio(
    servicio_id: int,
    data: ServicioUpdateSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Actualiza un servicio (solo el proveedor dueño)
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        servicio = session.query(ServicioModel).filter(
            ServicioModel.id == servicio_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado o no autorizado"
            )
        
        # Actualizar solo campos proporcionados
        if data.nombre is not None:
            servicio.nombre = data.nombre
        if data.descripcion is not None:
            servicio.descripcion = data.descripcion
        if data.categoria is not None:
            servicio.categoria = data.categoria
        
        from datetime import datetime
        servicio.updated_at = datetime.utcnow()
        
        session.commit()
        session.refresh(servicio)
        
        return ServicioResponse.model_validate(servicio)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar servicio"
        )


@router.delete('/{servicio_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio(
    servicio_id: int,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Desactiva un servicio (soft delete)
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        servicio = session.query(ServicioModel).filter(
            ServicioModel.id == servicio_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Servicio no encontrado o no autorizado"
            )
        
        servicio.is_active = False
        session.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar servicio"
        )

@router.get('/proveedores', response_model=List[dict])
def listar_proveedores(session: Session = Depends(get_session)):
    """
    Lista todos los proveedores que tienen servicios activos
    """
    try:
        from app.infrastructure.db.models.proveedor_model import ProveedorModel
        
        proveedores = session.query(
            ProveedorModel.id,
            ProveedorModel.nombre,
            ProveedorModel.apellido,
            ProveedorModel.especialidad,
            ProveedorModel.biografia
        ).join(
            ServicioModel, ProveedorModel.id == ServicioModel.proveedor_id
        ).filter(
            ProveedorModel.is_available == True,
            ServicioModel.is_active == True
        ).distinct().all()
        
        return [
            {
                "id": p.id,
                "nombre": f"{p.nombre} {p.apellido}",
                "especialidad": p.especialidad,
                "biografia": p.biografia
            }
            for p in proveedores
        ]
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error")

@router.get('/proveedor/{proveedor_id}', response_model=List[ServicioResponse])
def listar_servicios_proveedor(
    proveedor_id: int,
    session: Session = Depends(get_session)
):
    """
    Lista servicios de un proveedor específico
    """
    try:
        servicios = session.query(ServicioModel).filter(
            ServicioModel.proveedor_id == proveedor_id,
            ServicioModel.is_active == True
        ).all()
        
        return [ServicioResponse.model_validate(s) for s in servicios]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error")