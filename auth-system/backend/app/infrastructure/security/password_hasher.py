from passlib.context import CryptContext

from app.domain.services.i_password_hasher import IPasswordHasher

# Se mantiene sha256_crypt para seguir verificando los hashes ya almacenados.
_pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


class PasslibPasswordHasher(IPasswordHasher):
    """Implementación de IPasswordHasher con passlib."""

    def hash(self, password: str) -> str:
        return _pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)

