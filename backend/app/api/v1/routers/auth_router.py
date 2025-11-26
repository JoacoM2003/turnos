from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.schemas.user_schemas import (
    ClienteRegisterSchema,
    ProveedorRegisterSchema,
    ClienteUpdateSchema,
    ProveedorUpdateSchema,
    UserLoginSchema,
    TokenResponse,
    UserResponse,
    ClienteProfileResponse,
    ProveedorProfileResponse
)
from app.domain.use_cases.users.create_user import CreateUserUseCase, CreateUserDTO
from app.domain.use_cases.users.authenticate_user import AuthenticateUserUseCase, AuthenticateUserDTO
from app.domain.entities.cliente import Cliente
from app.domain.entities.proveedor import Proveedor
from app.infrastructure.repositories.cliente_repository import SQLAlchemyClienteRepository
from app.infrastructure.repositories.proveedor_repository import SQLAlchemyProveedorRepository
from app.api.v1.dependencies import get_create_user_use_case, get_authenticate_user_use_case
from app.infrastructure.db.database import get_session
from app.core.security import create_access_token, get_current_user, get_current_cliente, get_current_proveedor
from app.domain.entities.user import User


router = APIRouter(prefix='/auth', tags=['Autenticación'])


# ===== REGISTRO =====

@router.post('/register/cliente', response_model=ClienteProfileResponse, status_code=status.HTTP_201_CREATED)
def register_cliente(
    data: ClienteRegisterSchema,
    session: Session = Depends(get_session),
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    """
    Registra un nuevo cliente
    
    **Campos opcionales que se pueden completar después:**
    - `dni`: Documento de identidad
    - `fecha_nacimiento`: Fecha de nacimiento
    - `direccion`: Dirección del cliente
    - `telefono`: Número de teléfono
    """
    try:
        # 1) Crear usuario
        user_dto = CreateUserDTO(
            email=data.email,
            password=data.password,
            username=data.username,
            role="cliente"
        )
        user = use_case.execute(user_dto)
        
        # 2) Crear perfil de cliente
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = Cliente.create(
            user_id=user.id,
            nombre=data.nombre,
            apellido=data.apellido,
            telefono=data.telefono,
            dni=data.dni,
            fecha_nacimiento=data.fecha_nacimiento,
            direccion=data.direccion
        )
        saved_cliente = cliente_repo.save(cliente)
        
        return ClienteProfileResponse(
            id=user.id,
            email=user.email.value,
            username=user.username,
            role=user.role.value,
            is_active=user.is_active,
            cliente_id=saved_cliente.id,
            nombre=saved_cliente.nombre,
            apellido=saved_cliente.apellido,
            telefono=saved_cliente.telefono,
            dni=saved_cliente.dni,
            fecha_nacimiento=saved_cliente.fecha_nacimiento,
            direccion=saved_cliente.direccion
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error en registro de cliente: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar cliente"
        )


@router.post('/register/proveedor', response_model=ProveedorProfileResponse, status_code=status.HTTP_201_CREATED)
def register_proveedor(
    data: ProveedorRegisterSchema,
    session: Session = Depends(get_session),
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    """
    Registra un nuevo proveedor de servicios
    
    **Campos requeridos:**
    - `especialidad`: Tipo de servicio que ofrece (ej: Peluquería, Masajes)
    
    **Campos opcionales:**
    - `matricula`: Número de matrícula profesional
    - `biografia`: Descripción profesional
    - `telefono`: Número de contacto
    """
    try:
        # 1) Crear usuario
        user_dto = CreateUserDTO(
            email=data.email,
            password=data.password,
            username=data.username,
            role="proveedor"
        )
        user = use_case.execute(user_dto)
        
        # 2) Crear perfil de proveedor
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = Proveedor.create(
            user_id=user.id,
            nombre=data.nombre,
            apellido=data.apellido,
            especialidad=data.especialidad,
            matricula=data.matricula,
            telefono=data.telefono,
            biografia=data.biografia
        )
        saved_proveedor = proveedor_repo.save(proveedor)
        
        return ProveedorProfileResponse(
            id=user.id,
            email=user.email.value,
            username=user.username,
            role=user.role.value,
            is_active=user.is_active,
            proveedor_id=saved_proveedor.id,
            nombre=saved_proveedor.nombre,
            apellido=saved_proveedor.apellido,
            telefono=saved_proveedor.telefono,
            especialidad=saved_proveedor.especialidad,
            matricula=saved_proveedor.matricula,
            biografia=saved_proveedor.biografia,
            is_available=saved_proveedor.is_available
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error en registro de proveedor: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar proveedor"
        )


# ===== LOGIN =====

@router.post('/login', response_model=TokenResponse)
def login(
    data: UserLoginSchema,
    session: Session = Depends(get_session),
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case)
):
    """
    Inicia sesión con email y contraseña
    
    Devuelve un token JWT que debe incluirse en las peticiones protegidas:
    ```
    Authorization: Bearer <token>
    ```
    """
    try:
        auth_dto = AuthenticateUserDTO(
            email=data.email,
            password=data.password
        )
        user = use_case.execute(auth_dto)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Crear token
        access_token = create_access_token(subject=str(user.id))
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                email=user.email.value,
                username=user.username,
                role=user.role.value,
                is_active=user.is_active
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en login: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al iniciar sesión"
        )


# ===== PERFIL =====

@router.get('/me/cliente', response_model=ClienteProfileResponse)
def get_cliente_profile(
    current_user: User = Depends(get_current_cliente),
    session: Session = Depends(get_session)
):
    """
    Obtiene el perfil completo del cliente autenticado
    """
    try:
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = cliente_repo.get_by_user_id(current_user.id)
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de cliente no encontrado"
            )
        
        return ClienteProfileResponse(
            id=current_user.id,
            email=current_user.email.value,
            username=current_user.username,
            role=current_user.role.value,
            is_active=current_user.is_active,
            cliente_id=cliente.id,
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            telefono=cliente.telefono,
            dni=cliente.dni,
            fecha_nacimiento=cliente.fecha_nacimiento,
            direccion=cliente.direccion
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al obtener perfil de cliente: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener perfil"
        )


@router.get('/me/proveedor', response_model=ProveedorProfileResponse)
def get_proveedor_profile(
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Obtiene el perfil completo del proveedor autenticado
    """
    try:
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de proveedor no encontrado"
            )
        
        return ProveedorProfileResponse(
            id=current_user.id,
            email=current_user.email.value,
            username=current_user.username,
            role=current_user.role.value,
            is_active=current_user.is_active,
            proveedor_id=proveedor.id,
            nombre=proveedor.nombre,
            apellido=proveedor.apellido,
            telefono=proveedor.telefono,
            especialidad=proveedor.especialidad,
            matricula=proveedor.matricula,
            biografia=proveedor.biografia,
            is_available=proveedor.is_available
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al obtener perfil de proveedor: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener perfil"
        )


# ===== ACTUALIZAR PERFIL =====

@router.patch('/me/cliente', response_model=ClienteProfileResponse)
def update_cliente_profile(
    data: ClienteUpdateSchema,
    current_user: User = Depends(get_current_cliente),
    session: Session = Depends(get_session)
):
    """
    Actualiza el perfil del cliente autenticado
    
    **Aquí es donde el cliente puede completar su DNI, fecha de nacimiento, etc.**
    """
    try:
        cliente_repo = SQLAlchemyClienteRepository(session)
        cliente = cliente_repo.get_by_user_id(current_user.id)
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de cliente no encontrado"
            )
        
        # Actualizar solo los campos proporcionados
        if data.nombre is not None:
            cliente.nombre = data.nombre
        if data.apellido is not None:
            cliente.apellido = data.apellido
        if data.telefono is not None:
            cliente.telefono = data.telefono
        if data.dni is not None:
            cliente.dni = data.dni
        if data.fecha_nacimiento is not None:
            cliente.fecha_nacimiento = data.fecha_nacimiento
        if data.direccion is not None:
            cliente.direccion = data.direccion
        
        from datetime import datetime, timezone
        cliente.updated_at = datetime.now(timezone.utc)
        
        updated_cliente = cliente_repo.save(cliente)
        
        return ClienteProfileResponse(
            id=current_user.id,
            email=current_user.email.value,
            username=current_user.username,
            role=current_user.role.value,
            is_active=current_user.is_active,
            cliente_id=updated_cliente.id,
            nombre=updated_cliente.nombre,
            apellido=updated_cliente.apellido,
            telefono=updated_cliente.telefono,
            dni=updated_cliente.dni,
            fecha_nacimiento=updated_cliente.fecha_nacimiento,
            direccion=updated_cliente.direccion
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al actualizar perfil: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar perfil"
        )


@router.patch('/me/proveedor', response_model=ProveedorProfileResponse)
def update_proveedor_profile(
    data: ProveedorUpdateSchema,
    current_user: User = Depends(get_current_proveedor),
    session: Session = Depends(get_session)
):
    """
    Actualiza el perfil del proveedor autenticado
    """
    try:
        proveedor_repo = SQLAlchemyProveedorRepository(session)
        proveedor = proveedor_repo.get_by_user_id(current_user.id)
        
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil de proveedor no encontrado"
            )
        
        # Actualizar solo los campos proporcionados
        if data.nombre is not None:
            proveedor.nombre = data.nombre
        if data.apellido is not None:
            proveedor.apellido = data.apellido
        if data.telefono is not None:
            proveedor.telefono = data.telefono
        if data.especialidad is not None:
            proveedor.especialidad = data.especialidad
        if data.matricula is not None:
            proveedor.matricula = data.matricula
        if data.biografia is not None:
            proveedor.biografia = data.biografia
        
        from datetime import datetime, timezone
        proveedor.updated_at = datetime.now(timezone.utc)
        
        updated_proveedor = proveedor_repo.save(proveedor)
        
        return ProveedorProfileResponse(
            id=current_user.id,
            email=current_user.email.value,
            username=current_user.username,
            role=current_user.role.value,
            is_active=current_user.is_active,
            proveedor_id=updated_proveedor.id,
            nombre=updated_proveedor.nombre,
            apellido=updated_proveedor.apellido,
            telefono=updated_proveedor.telefono,
            especialidad=updated_proveedor.especialidad,
            matricula=updated_proveedor.matricula,
            biografia=updated_proveedor.biografia,
            is_available=updated_proveedor.is_available
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al actualizar perfil: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar perfil"
        )