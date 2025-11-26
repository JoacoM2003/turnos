from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone

from app.application.schemas.reserva_schemas import (
    ReservaCreateSchema,
    ReservaResponse,
    ReservaDetailResponse,
    PagoReservaSchema,
    CancelarReservaSchema,
    ConfirmarPagoSchema,
    MarcarNoAsistioSchema
)
from app.infrastructure.db.database import get_session
from app.infrastructure.db.models.reserva_model import ReservaModel
from app.infrastructure.db.models.recurso_model import RecursoModel
from app.infrastructure.db.models.servicio_model import ServicioModel
from app.infrastructure.db.models.horario_disponible_model import HorarioDisponibleModel
from app.infrastructure.db.models.cliente_model import ClienteModel
from app.core.security import get_current_cliente, get_current_proveedor
from app.domain.entities.user import User

router = APIRouter(prefix='/reservas', tags=['Reservas'])


@router.post('/', response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(
    data: ReservaCreateSchema,
    current_user: User = Depends(get_current_cliente),
    session: Session = Depends(get_session)
):
    """
    Crea una nueva reserva con opción de seña
    """
    try:
        from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = cliente_repo.get_by_user_id(current_user.id)
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Perfil de cliente no encontrado")
        
        # Verificar recurso
        recurso = session.query(RecursoModel).filter(
            RecursoModel.id == data.recurso_id,
            RecursoModel.is_active == True
        ).first()
        
        if not recurso:
            raise HTTPException(status_code=404, detail="Recurso no disponible")
        
        # Calcular fecha fin
        fecha_hora_fin = data.fecha_hora_inicio + timedelta(minutes=data.duracion_minutos)
        
        # Verificar disponibilidad (CRÍTICO: que no haya reservas confirmadas/pendientes)
        reservas_existentes = session.query(ReservaModel).filter(
            ReservaModel.recurso_id == data.recurso_id,
            ReservaModel.estado.in_(['pendiente', 'confirmada']),
            ReservaModel.fecha_hora_inicio < fecha_hora_fin,
            ReservaModel.fecha_hora_fin > data.fecha_hora_inicio
        ).count()
        
        if reservas_existentes > 0:
            raise HTTPException(status_code=400, detail="El horario ya está reservado")
        
        # Buscar precio
        fecha_inicio = data.fecha_hora_inicio
        if fecha_inicio.tzinfo is None:
            fecha_inicio = fecha_inicio.replace(tzinfo=timezone.utc)
        
        dia_semana = fecha_inicio.weekday()
        hora = fecha_inicio.time()
        
        horario = session.query(HorarioDisponibleModel).filter(
            HorarioDisponibleModel.recurso_id == data.recurso_id,
            HorarioDisponibleModel.dia_semana == dia_semana,
            HorarioDisponibleModel.hora_inicio <= hora,
            HorarioDisponibleModel.hora_fin > hora,
            HorarioDisponibleModel.is_active == True
        ).first()
        
        if not horario:
            raise HTTPException(status_code=400, detail="No hay horario disponible")
        
        precio_total = horario.precio
        
        # Calcular saldo
        seña = data.seña or 0
        if seña > precio_total:
            raise HTTPException(status_code=400, detail="La seña no puede ser mayor al precio total")
        
        saldo_pendiente = precio_total - seña
        pago_completo = saldo_pendiente == 0
        
        # Crear reserva
        reserva = ReservaModel(
            cliente_id=cliente.id,
            recurso_id=data.recurso_id,
            fecha_hora_inicio=fecha_inicio,
            fecha_hora_fin=fecha_hora_fin,
            duracion_minutos=data.duracion_minutos,
            precio_total=precio_total,
            seña=seña if seña > 0 else None,
            saldo_pendiente=saldo_pendiente,
            metodo_pago=data.metodo_pago,
            pago_completo=pago_completo,
            pago_confirmado=False,
            notas_cliente=data.notas_cliente
        )
        
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        
        return ReservaResponse.model_validate(reserva)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get('/mis-reservas', response_model=List[ReservaDetailResponse])
def listar_mis_reservas(
    estado: str = None,
    current_user: User = Depends(get_current_cliente),
    session: Session = Depends(get_session)
):
    """
    Lista las reservas del cliente autenticado
    
    **Filtros opcionales:**
    - `estado`: pendiente, confirmada, cancelada, completada
    """
    try:
        from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = cliente_repo.get_by_user_id(current_user.id)
        
        query = session.query(
            ReservaModel,
            RecursoModel.nombre.label('recurso_nombre'),
            ServicioModel.nombre.label('servicio_nombre'),
            ClienteModel.nombre.label('cliente_nombre')
        ).join(
            RecursoModel, ReservaModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).join(
            ClienteModel, ReservaModel.cliente_id == ClienteModel.id
        ).filter(
            ReservaModel.cliente_id == cliente.id
        )
        
        if estado:
            query = query.filter(ReservaModel.estado == estado)
        
        resultados = query.order_by(ReservaModel.fecha_hora_inicio.desc()).all()
        
        return [
            ReservaDetailResponse(
                id=r.ReservaModel.id,
                cliente_id=r.ReservaModel.cliente_id,
                recurso_id=r.ReservaModel.recurso_id,
                fecha_hora_inicio=r.ReservaModel.fecha_hora_inicio,
                fecha_hora_fin=r.ReservaModel.fecha_hora_fin,
                duracion_minutos=r.ReservaModel.duracion_minutos,
                estado=r.ReservaModel.estado,
                precio_total=r.ReservaModel.precio_total,
                seña=r.ReservaModel.seña,
                saldo_pendiente=r.ReservaModel.saldo_pendiente,
                pago_completo=r.ReservaModel.pago_completo,
                notas_cliente=r.ReservaModel.notas_cliente,
                created_at=r.ReservaModel.created_at,
                recurso_nombre=r.recurso_nombre,
                servicio_nombre=r.servicio_nombre,
                cliente_nombre=f"{r.cliente_nombre}"
            )
            for r in resultados
        ]
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar reservas"
        )


@router.get('/{reserva_id}', response_model=ReservaDetailResponse)
def obtener_reserva(
    reserva_id: int,
    current_user: User = Depends(get_current_cliente),
    session: Session = Depends(get_session)
):
    """
    Obtiene una reserva específica (solo el cliente dueño)
    """
    try:
        from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = cliente_repo.get_by_user_id(current_user.id)
        
        resultado = session.query(
            ReservaModel,
            RecursoModel.nombre.label('recurso_nombre'),
            ServicioModel.nombre.label('servicio_nombre'),
            ClienteModel.nombre.label('cliente_nombre')
        ).join(
            RecursoModel, ReservaModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).join(
            ClienteModel, ReservaModel.cliente_id == ClienteModel.id
        ).filter(
            ReservaModel.id == reserva_id,
            ReservaModel.cliente_id == cliente.id
        ).first()
        
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        return ReservaDetailResponse(
            id=resultado.ReservaModel.id,
            cliente_id=resultado.ReservaModel.cliente_id,
            recurso_id=resultado.ReservaModel.recurso_id,
            fecha_hora_inicio=resultado.ReservaModel.fecha_hora_inicio,
            fecha_hora_fin=resultado.ReservaModel.fecha_hora_fin,
            duracion_minutos=resultado.ReservaModel.duracion_minutos,
            estado=resultado.ReservaModel.estado,
            precio_total=resultado.ReservaModel.precio_total,
            seña=resultado.ReservaModel.seña,
            saldo_pendiente=resultado.ReservaModel.saldo_pendiente,
            pago_completo=resultado.ReservaModel.pago_completo,
            notas_cliente=resultado.ReservaModel.notas_cliente,
            created_at=resultado.ReservaModel.created_at,
            recurso_nombre=resultado.recurso_nombre,
            servicio_nombre=resultado.servicio_nombre,
            cliente_nombre=resultado.cliente_nombre
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener reserva"
        )


@router.patch('/{reserva_id}/cancelar', response_model=ReservaResponse)
def cancelar_reserva(
    reserva_id: int,
    data: CancelarReservaSchema,
    current_user: User = Depends(get_current_cliente),
    session: Session = Depends(get_session)
):
    """
    Cancela una reserva (solo el cliente dueño)
    """
    try:
        from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = cliente_repo.get_by_user_id(current_user.id)
        
        reserva = session.query(ReservaModel).filter(
            ReservaModel.id == reserva_id,
            ReservaModel.cliente_id == cliente.id
        ).first()
        
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        if reserva.estado in ['cancelada', 'completada']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede cancelar una reserva {reserva.estado}"
            )
        
        reserva.estado = 'cancelada'
        reserva.motivo_cancelacion = data.motivo
        reserva.fecha_cancelacion = datetime.now(timezone.utc)
        
        session.commit()
        session.refresh(reserva)
        
        return ReservaResponse.model_validate(reserva)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cancelar reserva"
        )


@router.patch('/{reserva_id}/pago', response_model=ReservaResponse)
def registrar_pago(
    reserva_id: int,
    data: PagoReservaSchema,
    current_user: User = Depends(get_current_cliente),
    session: Session = Depends(get_session)
):
    """
    Registra un pago para una reserva (seña o pago completo)
    """
    try:
        from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = cliente_repo.get_by_user_id(current_user.id)
        
        reserva = session.query(ReservaModel).filter(
            ReservaModel.id == reserva_id,
            ReservaModel.cliente_id == cliente.id
        ).first()
        
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva no encontrada"
            )
        
        if reserva.estado == 'cancelada':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede registrar pago en una reserva cancelada"
            )
        
        # Registrar pago
        if data.es_pago_completo:
            reserva.seña = data.monto
            reserva.saldo_pendiente = 0
            reserva.pago_completo = True
        else:
            reserva.seña = data.monto
            reserva.saldo_pendiente = reserva.precio_total - data.monto
        
        reserva.metodo_pago = data.metodo_pago
        
        session.commit()
        session.refresh(reserva)
        
        return ReservaResponse.model_validate(reserva)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar pago"
        )


@router.get('/proveedor/todas', response_model=List[ReservaDetailResponse])
def listar_reservas_proveedor(
    estado: str = None,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Lista todas las reservas del proveedor
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        query = session.query(
            ReservaModel,
            RecursoModel.nombre.label('recurso_nombre'),
            ServicioModel.nombre.label('servicio_nombre'),
            ClienteModel.nombre.label('cliente_nombre')
        ).join(
            RecursoModel, ReservaModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).join(
            ClienteModel, ReservaModel.cliente_id == ClienteModel.id
        ).filter(
            ServicioModel.proveedor_id == proveedor.id
        )
        
        if estado:
            query = query.filter(ReservaModel.estado == estado)
        
        resultados = query.order_by(ReservaModel.fecha_hora_inicio.desc()).all()
        
        return [
            ReservaDetailResponse(
                id=r.ReservaModel.id,
                cliente_id=r.ReservaModel.cliente_id,
                recurso_id=r.ReservaModel.recurso_id,
                fecha_hora_inicio=r.ReservaModel.fecha_hora_inicio,
                fecha_hora_fin=r.ReservaModel.fecha_hora_fin,
                duracion_minutos=r.ReservaModel.duracion_minutos,
                estado=r.ReservaModel.estado,
                precio_total=r.ReservaModel.precio_total,
                seña=r.ReservaModel.seña,
                saldo_pendiente=r.ReservaModel.saldo_pendiente,
                pago_completo=r.ReservaModel.pago_completo,
                notas_cliente=r.ReservaModel.notas_cliente,
                created_at=r.ReservaModel.created_at,
                recurso_nombre=r.recurso_nombre,
                servicio_nombre=r.servicio_nombre,
                cliente_nombre=r.cliente_nombre
            )
            for r in resultados
        ]
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar reservas"
        )


@router.patch('/proveedor/{reserva_id}/confirmar', response_model=ReservaResponse)
def confirmar_reserva_proveedor(
    reserva_id: int,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """Confirma una reserva"""
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        reserva = session.query(ReservaModel).join(
            RecursoModel, ReservaModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            ReservaModel.id == reserva_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not reserva:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
        
        if reserva.estado != 'pendiente':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo se pueden confirmar reservas pendientes")
        
        reserva.estado = 'confirmada'
        session.commit()
        session.refresh(reserva)
        
        return ReservaResponse.model_validate(reserva)
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error")


@router.patch('/proveedor/{reserva_id}/completar', response_model=ReservaResponse)
def completar_reserva_proveedor(
    reserva_id: int,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """Marca una reserva como completada"""
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        reserva = session.query(ReservaModel).join(
            RecursoModel, ReservaModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            ReservaModel.id == reserva_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not reserva:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
        
        if reserva.estado not in ['confirmada', 'en_curso']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Solo se pueden completar reservas confirmadas")
        
        reserva.estado = 'completada'
        session.commit()
        session.refresh(reserva)
        
        return ReservaResponse.model_validate(reserva)
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error")

@router.patch('/{reserva_id}/pago', response_model=ReservaResponse)
def registrar_pago_adicional(
    reserva_id: int,
    data: PagoReservaSchema,
    current_user: User = Depends(get_current_cliente),
    session: Session = Depends(get_session)
):
    """
    Registra un pago adicional (para completar el saldo)
    """
    try:
        from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = cliente_repo.get_by_user_id(current_user.id)
        
        reserva = session.query(ReservaModel).filter(
            ReservaModel.id == reserva_id,
            ReservaModel.cliente_id == cliente.id
        ).first()
        
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
        if reserva.estado == 'cancelada':
            raise HTTPException(status_code=400, detail="No se puede pagar una reserva cancelada")
        
        # Actualizar pago
        seña_actual = reserva.seña or 0
        seña_nueva = seña_actual + data.monto
        
        if seña_nueva > reserva.precio_total:
            raise HTTPException(status_code=400, detail="El monto total supera el precio")
        
        reserva.seña = seña_nueva
        reserva.saldo_pendiente = reserva.precio_total - seña_nueva
        reserva.pago_completo = reserva.saldo_pendiente == 0
        reserva.metodo_pago = data.metodo_pago
        
        if data.confirmado_por_proveedor:
            reserva.pago_confirmado = True
        
        session.commit()
        session.refresh(reserva)
        
        return ReservaResponse.model_validate(reserva)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar pago")


@router.patch('/proveedor/{reserva_id}/confirmar-pago', response_model=ReservaResponse)
def confirmar_pago_reserva(
    reserva_id: int,
    data: ConfirmarPagoSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    El proveedor confirma que recibió el pago
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        reserva = session.query(ReservaModel).join(
            RecursoModel, ReservaModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            ReservaModel.id == reserva_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
        reserva.pago_confirmado = data.pago_confirmado
        reserva.notas_pago = data.notas_pago
        
        session.commit()
        session.refresh(reserva)
        
        return ReservaResponse.model_validate(reserva)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error")



@router.patch('/proveedor/{reserva_id}/no-asistio', response_model=ReservaResponse)
def marcar_no_asistio(
    reserva_id: int,
    data: MarcarNoAsistioSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Marca que el cliente no asistió a la reserva
    """
    try:
        from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        reserva = session.query(ReservaModel).join(
            RecursoModel, ReservaModel.recurso_id == RecursoModel.id
        ).join(
            ServicioModel, RecursoModel.servicio_id == ServicioModel.id
        ).filter(
            ReservaModel.id == reserva_id,
            ServicioModel.proveedor_id == proveedor.id
        ).first()
        
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
        # Solo se puede marcar como no asistió si estaba confirmada y ya pasó la fecha
        if reserva.estado != 'confirmada':
            raise HTTPException(status_code=400, detail="Solo reservas confirmadas")
        
        now = datetime.now(timezone.utc)
        if reserva.fecha_hora_inicio > now:
            raise HTTPException(status_code=400, detail="La reserva aún no ha pasado")
        
        reserva.estado = 'no_asistio'
        if data.notas:
            reserva.notas_internas = data.notas
        
        session.commit()
        session.refresh(reserva)
        
        return ReservaResponse.model_validate(reserva)
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error")