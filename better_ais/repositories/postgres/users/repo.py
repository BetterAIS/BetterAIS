from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.queryset import QuerySet
from .model import User


class UserRepository:
    model = User

    async def create(self, **kwargs) -> User:
        return await self.model.create(**kwargs)

    async def get(self, **kwargs) -> User:
        return await self.model.get(**kwargs)

    async def filter(self, **kwargs) -> QuerySet:
        return self.model.filter(**kwargs)

    async def update(self, instance: User, **kwargs) -> None:
        await instance.update_from_dict(kwargs)

    async def delete(self, instance: User) -> None:
        await instance.delete()

    async def all(self) -> QuerySet:
        return self.model.all()

    async def count(self, **kwargs) -> int:
        return await self.model.filter(**kwargs).count()

    async def exists(self, **kwargs) -> bool:
        return await self.model.filter(**kwargs).exists()

    async def to_pydantic(self, instance: User):
        return await pydantic_model_creator(User)(instance)
