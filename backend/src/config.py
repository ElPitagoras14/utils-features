from dotenv import find_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class GeneralSettings(BaseSettings):
    AUTH_SECRET: str
    AUTH_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=find_dotenv(filename=".env", usecwd=True),
        env_file_encoding="utf-8",
        extra="ignore",
    )


general_settings = GeneralSettings()
