from pydantic import BaseSettings

class OpenAiSettings(BaseSettings):
    api_key: str
    model: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"
