from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    TG_TOKEN: str
    BASE_URL: str
    TG_TEST_MODE: bool = Field(False)
    TG_BOT_URL: str

    @property
    def search_url(self):
        return f"{self.BASE_URL}/tg/search"

    @property
    def webhook_url(self):
        return f"{self.BASE_URL}/tg/{self.TG_TOKEN}"

    @property
    def new_tg(self):
        return f"{self.BASE_URL}/new-tg/menu"


settings = Settings()  # type: ignore
