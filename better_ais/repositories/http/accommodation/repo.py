from .model import AccUser
from .source.accommodation import AccommodationSource


class AccommodationRepository:
    async def create(self, **kwargs) -> None:
        raise NotImplementedError

    async def get(self, login: str, password: str) -> AccUser:
        source = AccommodationSource(login, password)
        await source.login()
        return AccUser.from_dataclass(await source.get_user())

    async def filter(self, **kwargs) -> None:
        raise NotImplementedError

    async def update(self, instance: AccUser, **kwargs) -> None:
        raise NotImplementedError

    async def delete(self, instance: AccUser) -> None:
        raise NotImplementedError

    async def all(self) -> None:
        raise NotImplementedError

    async def count(self, **kwargs) -> None:
        raise NotImplementedError

    async def exists(self, **kwargs) -> None:
        raise NotImplementedError

    async def to_pydantic(self, instance: AccUser) -> None:
        raise NotImplementedError
