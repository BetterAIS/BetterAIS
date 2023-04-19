from pydantic import BaseSettings, Field

class LdapSettings(BaseSettings):
    basedn = Field(..., env="LDAP_BASEDN")
    attrs = Field(..., env="LDAP_ATTRS")
    server = Field(..., env="LDAP_SERVER")
    
    class Config:
        case_sensitive = False
