from better_ais.di.configuration import Configuration
from better_ais.di.repositories import RepositoriesContainer
from better_ais.di.controllers import ControllersContainer
from functools import cached_property
from tortoise import Tortoise
from fastapi import FastAPI

class Core:
    def __init__(self): ...
    
    @cached_property
    def configuration(self) -> Configuration:
        return Configuration()

    @cached_property
    def repositories(self):
        return RepositoriesContainer(self.configuration.core_settings, self.configuration.openai_settings, self.configuration.ldap_settings)

    @cached_property
    def controllers(self):
        return ControllersContainer(self.repositories, self.configuration.core_settings)

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
            ]}
        )
        
        await Tortoise.generate_schemas()
        return Tortoise

core_di = Core()
