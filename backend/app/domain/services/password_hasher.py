from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """
    Interface para servicios de hashing de contraseñas.
    Permite cambiar la implementación sin afectar el dominio.
    """

    @abstractmethod
    def hash(self, plain_password: str) -> str:
        """Hashea una contraseña en texto plano"""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña coincide con su hash"""
        pass