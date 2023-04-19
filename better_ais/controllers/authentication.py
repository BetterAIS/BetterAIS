from dataclasses import dataclass
import uuid
import jwt

from datetime import datetime, timedelta
from passlib.context import CryptContext
from better_ais.config.core import CoreSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthenticationServiceException(Exception):
    pass

class AccessTokenExpiredException(AuthenticationServiceException):
    pass

class RefreshTokenExpiredException(AuthenticationServiceException):
    pass

class RevokedTokenAlreadyUsedException(AuthenticationServiceException):
    pass

class InvalidTokenException(AuthenticationServiceException):
    pass


@dataclass
class TokenData:
    user_id: int
    magic: str
    exp: datetime
    token_type: str
    
    def __post_init__(self):
        if not isinstance(self.exp, datetime):
            self.exp = datetime.fromtimestamp(self.exp)
        
        if self.token_type not in ["access", "refresh"]:
            raise InvalidTokenException("Token type is invalid")

class AuthenticationService:
    def __init__(self, core: CoreSettings):
        self.__core = core
        self.__used_magics: list[str] = []
        self.__revoked_magics: list[str] = []

    def __gen_magic(self) -> str:
        magic = str(uuid.uuid4())
        self.__used_magics.append(magic)
        return magic
    
    def __gen_token(self, user_id: int, magic: str, token_type: str) -> str:
        payload = {
            "user_id": user_id,
            "magic": magic,
            "exp": datetime.utcnow() + (
                timedelta(minutes=self.__core.ACCESS_TOKEN_EXPIRE_MINUTES) 
                    if token_type == "access" else 
                timedelta(minutes=self.__core.REFRESH_TOKEN_EXPIRE_MINUTES)
            ),
            "token_type": token_type
        }
        return jwt.encode(payload, self.__core.jwt_secret, algorithm=self.__core.jwt_algorithm).decode("utf-8")
    
    def __decode_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, self.__core.jwt_secret, algorithms=[self.__core.jwt_algorithm])
            return TokenData(**payload)
        except jwt.ExpiredSignatureError:
            raise AccessTokenExpiredException("Access token is expired")
    
    def __is_token_revoked(self, token: str) -> bool:
        decoded = self.__decode_token(token)
        if decoded.magic in self.__revoked_magics:
            return True
        return False
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    def create_access_token(self, user_id: int) -> str:
        return self.__gen_token(user_id, self.__gen_magic(), "access")
    
    def create_refresh_token(self, user_id: int) -> str:
        return self.__gen_token(user_id, self.__gen_magic(), "refresh")
    
    def generete_pair(self, user_id: int) -> tuple[str, str]:
        return self.create_access_token(user_id), self.create_refresh_token(user_id)
    
    def revoke_token(self, token: str) -> None:
        decoded = self.__decode_token(token)
        self.__revoked_magics.append(decoded.magic)
    
    def use_refresh_token(self, token: str) -> tuple[str, str]:
        decoded = self.__decode_token(token)
        if decoded.token_type != "refresh":
            raise AuthenticationServiceException("Token is not a refresh token")
        self.validate_token(token)
        self.revoke_token(token)
        return self.generete_pair(decoded.user_id)
    
    def validate_token(self, token: str) -> TokenData:
        decoded = self.__decode_token(token)
        if self.__is_token_revoked(token):
            raise AuthenticationServiceException("Token is revoked")
        return decoded
    
    def get_user_id(self, token: str) -> int:
        return self.validate_token(token).user_id
