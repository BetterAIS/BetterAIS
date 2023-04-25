import asyncio

from .source.auth_ldap import Ldap3Auth
from .model import User


class LdapRepository:
    def __init__(self, ldap_settings):
        self.ldap_settings = ldap_settings
    
    async def create(self, **kwargs) -> None:
        raise NotImplementedError

    async def get(self, login: str, password: str) -> User:
        return await asyncio.to_thread(Ldap3Auth(self.ldap_settings).authenticate_ldap, login, password)

    async def filter(self, **kwargs) -> None:
        raise NotImplementedError

    async def update(self, instance: User, **kwargs) -> None:
        raise NotImplementedError

    async def delete(self, instance: User) -> None:
        raise NotImplementedError

    async def all(self) -> None:
        raise NotImplementedError

    async def count(self, **kwargs) -> None:
        raise NotImplementedError

    async def exists(self, **kwargs) -> None:
        raise NotImplementedError

    async def to_pydantic(self, instance: User) -> None:
        raise NotImplementedError
