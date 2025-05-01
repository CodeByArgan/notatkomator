from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    cors_origins: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    @property
    def db_url(self) -> str:
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


env_settings = EnvSettings()
