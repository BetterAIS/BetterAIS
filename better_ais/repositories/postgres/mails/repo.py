from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.queryset import QuerySet
from .model import Mail


class MailRepository:
    model = Mail

    async def create(self, **kwargs) -> Mail:
        return await self.model.create(**kwargs)

    async def get(self, **kwargs) -> Mail:
        return await self.model.get(**kwargs)

    async def get_all(self, **kwargs) -> list[Mail]:
        return [
            i async for i in self.model.filter(**kwargs)
        ]

    async def filter(self, **kwargs) -> QuerySet[Mail]:
        return self.model.filter(**kwargs)

    async def update(self, instance: Mail, **kwargs) -> None:
        await instance.update_from_dict(kwargs)

    async def delete(self, instance: Mail) -> None:
        await instance.delete()

    async def all(self) -> QuerySet:
        return self.model.all()

    async def count(self, **kwargs) -> int:
        return await self.model.filter(**kwargs).count()

    async def exists(self, **kwargs) -> bool:
        return await self.model.filter(**kwargs).exists()

    async def to_pydantic(self, instance: Mail):
        return await pydantic_model_creator(Mail)(instance)
