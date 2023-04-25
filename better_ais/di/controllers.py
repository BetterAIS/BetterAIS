from functools import cached_property
from better_ais.di.repositories import RepositoriesContainer
from better_ais.controllers.authentication import AuthenticationController
from better_ais.controllers.users import UsersController

class ControllersContainer:
    def __init__(self, repos: RepositoriesContainer, core):
        self.repos = repos
        self.core = core
    
    @cached_property
    def authentication(self) -> AuthenticationController:
        return AuthenticationController(self.core)

    @cached_property
    def users(self) -> UsersController:
        return UsersController(
            self.repos.pg_users_repository,
            self.repos.pg_mails_repository,
            self.repos.pg_documents_repository,
            self.repos.ldap_repository,
            self.repos.accommodation_repository,
            self.repos.ais_repository
        )