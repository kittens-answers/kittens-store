from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    TG_TOKEN: str
    BASE_URL: str
    TG_TEST_MODE: bool = Field(False)
    TG_BOT_URL: str

    @property
    def load_url(self):
        return f"{self.BASE_URL}/tg/load"

    @property
    def webhook_url(self):
        return f"{self.BASE_URL}/tg/{self.TG_TOKEN}"


settings = Settings()  # type: ignore
