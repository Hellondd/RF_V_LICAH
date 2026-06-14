# ⚠️ ВНИМАНИЕ: этот файл содержит только заготовки.
# Реализацию функций должен дописать backend-разработчик,
# используя passlib[bcrypt] и python-jose.

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """TODO: реализовать хеширование пароля"""
    # Пример: return pwd_context.hash(password)
    raise NotImplementedError("Backend developer must implement this")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """TODO: реализовать проверку пароля"""
    raise NotImplementedError("Backend developer must implement this")

def create_access_token(data: dict, expires_delta=None):
    """TODO: реализовать создание JWT"""
    raise NotImplementedError("Backend developer must implement this")