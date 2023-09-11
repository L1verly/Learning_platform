from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"])


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)
