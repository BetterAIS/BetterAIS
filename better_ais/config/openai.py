from pydantic import BaseSettings

class OpenAiSettings(BaseSettings):
    api_key: str
    model: str = "davinci"

    class Config:
        env_file = ".env"
