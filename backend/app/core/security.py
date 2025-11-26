from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.api.v1.dependencies import get_user_repository

security = HTTPBearer()


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[str]:
    """Decodifica un token JWT y retorna el subject (user_id)"""
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository)
) -> User:
    """Obtiene el usuario actual desde el token JWT"""
    token = credentials.credentials
    user_id = decode_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = user_repository.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    return user


async def get_current_cliente(current_user: User = Depends(get_current_user)) -> User:
    """Verifica que el usuario actual sea un cliente"""
    if current_user.role.value not in ["cliente", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo clientes pueden realizar esta acción"
        )
    return current_user


async def get_current_proveedor(current_user: User = Depends(get_current_user)) -> User:
    """Verifica que el usuario actual sea un proveedor"""
    if current_user.role.value not in ["proveedor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo proveedores pueden realizar esta acción"
        )
    return current_user