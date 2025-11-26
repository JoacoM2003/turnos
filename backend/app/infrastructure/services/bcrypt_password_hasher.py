import bcrypt
from app.domain.services.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    """
    Implementación de PasswordHasher usando bcrypt.
    """

    def hash(self, plain_password: str) -> str:
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        try:
            return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
        except ValueError:
            return False
