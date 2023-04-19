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
                'better_ais.repositories.postgres.mails.model',
                'better_ais.repositories.postgres.posts.model',
                'better_ais.repositories.postgres.roles.model',
                'better_ais.repositories.postgres.users.model',
                'better_ais.repositories.postgres.documents.model',
                'better_ais.repositories.postgres.shared_notes.model',
                'better_ais.repositories.postgres.user_settings.model',
            ]}
        )
        
        await Tortoise.generate_schemas()
        return Tortoise

core = Core()
