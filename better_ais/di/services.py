from functools import cached_property
from better_ais.config.core import CoreSettings
from better_ais.services.authentication import AuthenticationService

class ServiceContainer:
    def __init__(self, core: CoreSettings):
        self._core = core

    @cached_property
    def authentication_service(self) -> AuthenticationService:
        return AuthenticationService(self._core)

