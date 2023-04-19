import asyncio

from .source.auth_ldap import Ldap3Auth
from .model import User


class AccommodationRepository:
    async def create(self, **kwargs) -> None:
        raise NotImplementedError

    async def get(self, login: str, password: str) -> User:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor((login, password), Ldap3Auth().authenticate_ldap)

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
