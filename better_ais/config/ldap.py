from pydantic import BaseSettings, Field

class LdapSettings(BaseSettings):
    basedn: str = Field(..., env="LDAP_BASEDN")
    attrs: list[str] = Field(..., env="LDAP_ATTRS")
    server: str = Field(..., env="LDAP_SERVER")
    
    class Config:
        case_sensitive = False
