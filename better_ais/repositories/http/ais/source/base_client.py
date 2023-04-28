from abc import ABC, abstractmethod

class AISClient(ABC):
    @abstractmethod
    async def get_new_mails(self, username: str, password: str) -> list[dict]: ...
    
    @abstractmethod
    async def get_documents(self, username: str, password: str) -> list[dict]: ...

    @abstractmethod
    async def get_homeworks(self, username: str, password: str) -> list[dict]: ...

    @abstractmethod
    async def get_time_table(self, username: str, password: str) -> list[dict]: ...