from better_ais.config import CoreSettings
from better_ais.config import PostgresSettings
from better_ais.config import LdapSettings
from better_ais.config import OpenAiSettings
from functools import cached_property


class Configuration:
    @cached_property
    def core_settings(self) -> CoreSettings:
        return CoreSettings()
    
    @cached_property
    def postgres_settings(self) -> PostgresSettings:
        return PostgresSettings()
    
    @cached_property
    def ldap_settings(self) -> LdapSettings:
        return LdapSettings()

    @cached_property
    def openai_settings(self) -> OpenAiSettings:
        return OpenAiSettings()

