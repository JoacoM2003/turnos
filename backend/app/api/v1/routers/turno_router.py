# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.application.schemas.turno_schemas import TurnoCreateSchema, TurnoResponse
# from app.domain.use_cases.turnos.create_turno import CreateTurnoUseCase, CreateTurnoDTO
# from app.domain.entities.user import User
# from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
# from app.infrastructure.repositories.servicio_repository import SQLAlchemyServicioRepository
# from app.api.v1.dependencies import get_create_turno_use_case
# from app.infrastructure.db.database import get_session
# from app.core.security import get_current_cliente


# router = APIRouter(prefix='/turnos', tags=['Turnos'])


# @router.post('/', response_model=TurnoResponse, status_code=status.HTTP_201_CREATED)
# def crear_turno(
#     turno_data: TurnoCreateSchema,
#     current_user: User = Depends(get_current_cliente),
#     session: Session = Depends(get_session),
#     use_case: CreateTurnoUseCase = Depends(get_create_turno_use_case)
# ):
#     """
#     Crea un nuevo turno para el cliente autenticado
#     """
#     try:
#         # Obtener cliente del usuario actual
#         cliente_repo = SQLAlchemyClienteRepository(session)
#         cliente = cliente_repo.get_by_user_id(current_user.id)
        
#         if not cliente:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Cliente no encontrado"
#             )
        
#         # Verificar que el servicio existe y obtener su información
#         servicio_repo = SQLAlchemyServicioRepository(session)
#         servicio = servicio_repo.get_by_id(turno_data.servicio_id)
        
#         if not servicio:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Servicio no encontrado"
#             )
        
#         # Verificar que el proveedor del servicio coincide
#         if servicio.proveedor_id != turno_data.proveedor_id:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="El servicio no pertenece al proveedor seleccionado"
#             )
        
#         # Crear DTO con el cliente del usuario autenticado
#         dto = CreateTurnoDTO(
#             cliente_id=cliente.id,
#             proveedor_id=turno_data.proveedor_id,
#             servicio_id=turno_data.servicio_id,
#             fecha_hora=turno_data.fecha_hora,
#             duracion_minutos=servicio.duracion_minutos,
#             precio=servicio.precio,
#             notas_cliente=turno_data.notas_cliente
#         )
        
#         turno = use_case.execute(dto)
        
#         return TurnoResponse(
#             id=turno.id,
#             cliente_id=turno.cliente_id,
#             proveedor_id=turno.proveedor_id,
#             servicio_id=turno.servicio_id,
#             fecha_hora=turno.fecha_hora.value,
#             duracion_minutos=turno.duracion_minutos,
#             estado=turno.estado,
#             precio=turno.precio,
#             notas_cliente=turno.notas_cliente,
#             created_at=turno.created_at
#         )
        
#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error interno: {str(e)}"
#         )