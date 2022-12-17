from pydantic import BaseModel, BaseSettings


class Urls(BaseModel):
    menu: str


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    TG_TOKEN: str
    urls: Urls


settings = Settings()  # type: ignore
