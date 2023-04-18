from better_ais.di.configuration import Configuration
from better_ais.di.services import ServiceContainer
from functools import cached_property
from tortoise import Tortoise
from fastapi import FastAPI

class Core:
    def __init__(self): ...
    
    @cached_property
    def configuration(self) -> Configuration:
        return Configuration()

    @cached_property
    def services(self):
        return ServiceContainer(self.configuration.core_settings)

    @cached_property
    def app(self) -> FastAPI:
        return FastAPI(
            debug=self.configuration.core_settings.DEBUG,
        )
    
    @cached_property
    async def database(self):
        await Tortoise.init(
            db_url=self.configuration.postgres_settings.connection_string,
            modules={'models': [
                'better_ais.dao.postgres.user.model',
                'better_ais.dao.postgres.user_roles.model',
                'better_ais.dao.postgres.user_settings.model',
                'better_ais.dao.postgres.user_subjects.model',
                'better_ais.dao.postgres.timetable.model',
                'better_ais.dao.postgres.subject.model',
                'better_ais.dao.postgres.shared_note.model',
                'better_ais.dao.postgres.role.model',
                'better_ais.dao.postgres.post.model',
                'better_ais.dao.postgres.mail.model',
                'better_ais.dao.postgres.homework.model',
                'better_ais.dao.postgres.document.model',
                'better_ais.dao.postgres.comment.model',
            ]}
        )
        
        await Tortoise.generate_schemas()
        return Tortoise

core = Core()
