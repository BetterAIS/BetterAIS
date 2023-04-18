import jwt
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from better_ais.config.core import CoreSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:
    def __init__(self, core: CoreSettings):
        self._core = core

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create an access token with the given data and expiration time.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self._core.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._core.SECRET_KEY, algorithm=self._core.JWT_ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify the given plain password matches the given hashed password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Hash the given password using the configured password hashing algorithm.
        """
        return pwd_context.hash(password)

    def decode_access_token(self, token: str) -> Optional[dict]:
        """
        Decode the given access token and return its contents if valid.
        """
        try:
            decoded_token = jwt.decode(token, self._core.SECRET_KEY, algorithms=[self._core.JWT_ALGORITHM])
            return decoded_token
        except jwt.JWTError:
            return None
