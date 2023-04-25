import uuid
import jwt

from dataclasses import dataclass
from datetime import datetime, timedelta
from passlib.context import CryptContext
from better_ais.config.core import CoreSettings
from fastapi import Depends, HTTPException, status
from cryptography.fernet import Fernet

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthenticationServiceException(HTTPException):
    def __init__(self, detail: str = "Authentication service error"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

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
    login: str
    password: str
    
    def __post_init__(self):
        if not isinstance(self.exp, datetime):
            self.exp = datetime.fromtimestamp(self.exp)
        
        if self.token_type not in ["access", "refresh"]:
            raise InvalidTokenException("Token type is invalid")

class AuthenticationController:
    __key = Fernet.generate_key()
    
    def __init__(self, core: CoreSettings):
        self.__core = core
        self.__used_magics: list[str] = []
        self.__revoked_magics: list[str] = []
        
        self.__f = Fernet(self.__key)

    def __gen_magic(self) -> str:
        magic = str(uuid.uuid4())
        self.__used_magics.append(magic)
        return magic

    def __encrypt(self, data: str) -> str:
        return self.__f.encrypt(data.encode()).decode()

    def __decrypt(self, data: str) -> str:
        return self.__f.decrypt(data.encode()).decode()

    def __gen_token(self, user_id: int, login: str, passwords: str, magic: str, token_type: str) -> str:
        payload = {
            "user_id": user_id,
            "magic": magic,
            "exp": datetime.utcnow() + (
                timedelta(minutes=self.__core.ACCESS_TOKEN_EXPIRE_MINUTES) 
                    if token_type == "access" else 
                timedelta(minutes=self.__core.REFRESH_TOKEN_EXPIRE_MINUTES)
            ),
            "token_type": token_type,
            "login": self.__encrypt(login),
            "password": self.__encrypt(passwords)
        }
        encoded = jwt.encode(payload, self.__core.SECRET_KEY, algorithm=self.__core.JWT_ALGORITHM)
        return encoded
    
    def __decode_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, self.__core.SECRET_KEY, algorithms=[self.__core.JWT_ALGORITHM])
            res = TokenData(**payload)
            res.login = self.__decrypt(res.login)
            res.password = self.__decrypt(res.password)
            return res
        except:
            raise AccessTokenExpiredException("Access token is expired")
    
    def __is_token_revoked(self, token: str) -> bool:
        decoded = self.__decode_token(token)
        if decoded.magic in self.__revoked_magics:
            return True
        return False
    
    async def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    async def create_access_token(self, user_id: int, login: str, password: str) -> str:
        return self.__gen_token(user_id, login, password, self.__gen_magic(), "access")
    
    async def create_refresh_token(self, user_id: int, login: str, password: str) -> str:
        return self.__gen_token(user_id, login, password, self.__gen_magic(), "refresh")
    
    async def generete_pair(self, user_id: int, login: str, password: str) -> tuple[str, str]:
        return await self.create_access_token(user_id, login, password), await self.create_refresh_token(user_id, login, password)
    
    async def revoke_token(self, token: str) -> None:
        decoded = self.__decode_token(token)
        self.__revoked_magics.append(decoded.magic)
    
    async def use_refresh_token(self, token: str) -> tuple[str, str]:
        decoded = self.__decode_token(token)
        if decoded.token_type != "refresh":
            raise AuthenticationServiceException("Token is not a refresh token")
        await self.validate_token(token)
        await self.revoke_token(token)
        return await self.generete_pair(decoded.user_id, decoded.login, decoded.password)
    
    async def validate_token(self, token: str) -> TokenData:
        decoded = self.__decode_token(token)
        if self.__is_token_revoked(token):
            raise AuthenticationServiceException("Token is revoked")
        return decoded
    
    async def get_user_id(self, token: str) -> int:
        return (await self.validate_token(token)).user_id
    
    async def get_token_payload(self, token: str) -> TokenData:
        return await self.validate_token(token)
