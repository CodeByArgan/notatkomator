from uuid import UUID
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    cors_origins: str

    refresh_secret: str
    refresh_cookie_name: str
    refresh_token_expire_days: int

    descope_id: str
    debug: bool = False

    test_user_uuid: UUID

    @property
    def db_url(self) -> str:
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


env_settings = EnvSettings()
