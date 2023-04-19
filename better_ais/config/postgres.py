from pydantic import BaseSettings, Field

class PostgresSettings(BaseSettings):
    postgres_host: str = Field(...)
    postgres_port: int = Field(...)
    postgres_user: str = Field(...)
    postgres_password: str = Field(...)
    postgres_db: str = Field(...)

    @property
    def connection_string(self) -> str:
        return f"postgres://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        case_sensitive = False