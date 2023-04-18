from .model import User


class UserRepo:
    async def create(self, user: User) -> User | None:
        return await User.create(**user.dict())

    async def get(self, user_id: int) -> User | None:
        return await User.get(id=user_id)

    async def get_all(self) -> list[User]:
        return await User.all()

    async def update(self, user: User) -> User | None:
        await User.filter(id=user.id).update(**user.dict(exclude_unset=True))
        return await self.get(user.id)
    
    async def delete(self, user_id: int) -> None:
        await User.filter(id=user_id).delete()

    async def get_by(self, **kwargs) -> User | None:
        return await User.get(**kwargs)
