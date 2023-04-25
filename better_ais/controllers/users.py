"""
Тут мы делаем:
    - мейлы
    - документы
    - хомворки
    - убитование
    - и т.д.
"""
from better_ais.repositories.postgres.users import UserRepository, User as PgUser
from better_ais.repositories.postgres.mails import MailRepository, Mail as PgMail
from better_ais.repositories.postgres.documents import DocumentRepository, Document as PgDocument

from better_ais.repositories.ldap.stu import LdapRepository, User as LdapUser
from better_ais.repositories.http.accommodation import AccommodationRepository, AccUser
from better_ais.repositories.http.ais import Mail, Document, Homework, AISRepository, TimeTable


class UsersServiceException(Exception):
    pass

class UsersController:
    def __init__(self, 
                 users_repo_pg: UserRepository, 
                 mails_repo_pg: MailRepository,
                 documents_repo_pg: DocumentRepository,
                 users_repo_ldap: LdapRepository,
                 users_repo_accommodation: AccommodationRepository,
                 ais_repo: AISRepository
                 ):
        self.users_repo_pg = users_repo_pg
        self.mails_repo_pg = mails_repo_pg
        self.documents_repo_pg = documents_repo_pg
        
        self.users_repo_ldap = users_repo_ldap
        self.users_repo_accommodation = users_repo_accommodation
        self.ais_repo = ais_repo
    
    async def create_user(self, login: str, password: str) -> PgUser:
        ldap_user = await self.users_repo_ldap.get(login, password)
        if not ldap_user.uisId:
            raise UsersServiceException("User not found")
        
        uis_id = "".join((i for i in ldap_user.uisId if i.isdigit()))
        try:
            pg_user = await self.users_repo_pg.get(id=uis_id)
        except:
            pg_user = await self.users_repo_pg.create(
                id=uis_id,
                ais_username=login,
                email=ldap_user.mail,
                is_verified=True
            )
        return pg_user
    
    async def get_user(self, login: str, password: str) -> PgUser:
        ldap_user = await self.users_repo_ldap.get(login, password)
        if not ldap_user.uisId:
            raise UsersServiceException("User not found")
        
        uis_id = "".join((i for i in ldap_user.uisId if i.isdigit()))
        pg_user = await self.users_repo_pg.get(id=uis_id)
        return pg_user

    async def get_user_accommodation(self, login: str, password: str) -> AccUser:
        acc_user = await self.users_repo_accommodation.get(login, password)
        if not acc_user:
            raise UsersServiceException("User not found")
        
        return acc_user

    async def get_user_new_mails(self, login: str, password: str) -> list[Mail]:
        pg_user = await self.get_user(login, password)
        if not pg_user:
            raise UsersServiceException("User not found")

        mails = await self.ais_repo.get_mails(pg_user.id, login, password)
        for mail in mails:
            await self.mails_repo_pg.create(
                id=mail.id,
                user=pg_user,
                sender=mail.sender,
                subject=mail.subject,
                body=mail.body,
                is_read=mail.is_read,
                created_at=mail.created_at,
                updated_at=mail.updated_at,
            )
        return mails

    async def get_user_mails(self, login: str, password: str) -> list[Mail]:
        pg_user = await self.get_user(login, password)
        if not pg_user:
            raise UsersServiceException("User not found")

        return [
            Mail(
                id=mail.id,
                user=pg_user.id,
                sender=mail.sender,
                subject=mail.subject,
                body=mail.body,
                is_read=mail.is_read,
                created_at=mail.created_at,
                updated_at=mail.updated_at,
            ) for mail in await (await self.mails_repo_pg.filter(user=pg_user)).all()
        ]
    
    async def get_user_new_documents(self, login: str, password: str) -> list[Document]:
        pg_user = await self.get_user(login, password)
        if not pg_user:
            raise UsersServiceException("User not found")
        
        documents = await self.ais_repo.get_documents(pg_user.id, login, password)
        for document in documents:
            await self.documents_repo_pg.create(
                id=document.id,
                user=pg_user,
                author=document.author,
                subject=document.subject,
                title=document.title,
                description=document.description,
                file_path=document.file_path,
                link=document.link,
                created_at=document.created_at,
                updated_at=document.updated_at,
            )
        return documents

    async def get_user_documents(self, login: str, password: str) -> list[Document]:
        pg_user = await self.get_user(login, password)
        if not pg_user:
            raise UsersServiceException("User not found")

        return [
            Document(
                id=document.id,
                user=pg_user.id,
                author=document.author,
                subject=document.subject,
                title=document.title,
                description=document.description,
                file_path=document.file_path,
                link=document.link,
                created_at=document.created_at,
                updated_at=document.updated_at,
            ) for document in await (await self.documents_repo_pg.filter(user=pg_user)).all()
        ]

    async def get_user_homeworks(self, login: str, password: str) -> list[Homework]:
        pg_user = await self.get_user(login, password)
        if not pg_user:
            raise UsersServiceException("User not found")
        
        homeworks = await self.ais_repo.get_homeworks(pg_user.id, login, password)
        return homeworks

    async def get_user_time_table(self, login: str, password: str) -> list[TimeTable]:
        pg_user = await self.get_user(login, password)
        if not pg_user:
            raise UsersServiceException("User not found")
        
        return await self.ais_repo.get_time_table(pg_user.id, login, password)
