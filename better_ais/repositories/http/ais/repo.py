from .model import Mail, Document, Homework, TimeTable
from .source import AISClient

class AISRepository(object):
    """AISRepository is a class that represents an AIS repository.

    It is used to retrieve AIS messages from AIS repository.
    """

    def __init__(self, ais_client: AISClient):
        """Initialize AISRepository.

        :param url: AIS repository URL
        :type url: str
        """
        self.ais_client = ais_client

    async def get_mails(self, user_id: int, username: str, password: str) -> list[Mail]:
        """Get AIS mails.
        """
        new_mails = await self.ais_client.get_new_mails(username, password)
        resilt = []
        for mail in new_mails:
            resilt.append(Mail(
                user=user_id,
                **mail
            ))
        return resilt

    async def get_documents(self, user_id: int, username: str, password: str) -> list[Document]:
        """Get AIS documents.
        """
        new_documents = await self.ais_client.get_documents(username, password)
        resilt = []
        for document in new_documents:
            resilt.append(Document(
                user=user_id,
                **document
            ))
        return resilt

    async def get_homeworks(self, user_id: int, username: str, password: str) -> list[Homework]:
        """Get AIS homeworks.
        """
        new_homeworks = await self.ais_client.get_homeworks(username, password)
        resilt = []
        for homework in new_homeworks:
            resilt.append(Homework(
                user=user_id,
                **homework
            ))
        return resilt

    async def get_time_table(self, user_id: int, username: str, password: str) -> list[TimeTable]:
        """Get AIS time table.
        """
        tt = await self.ais_client.get_time_table(username, password)
        resilt = []
        for day in tt:
            resilt.append(TimeTable(
                user=user_id,
                **day
            ))
        
        return resilt
