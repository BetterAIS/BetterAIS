from pydantic import BaseSettings, Field

class CoreSettings(BaseSettings):
    DEBUG: bool = Field(False)
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24 * 7)
    SECRET_KEY: str = Field("secret")
    JWT_ALGORITHM: str = Field("HS256")
    
    

    class Config:
        case_sensitive = False