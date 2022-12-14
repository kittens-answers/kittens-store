import uvicorn
from pydantic import BaseSettings
from pyngrok import ngrok


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    ngrok_set_auth_token: str
    ngrok_use: bool


settings = Settings()  # type: ignore

if __name__ == "__main__":
    if settings.ngrok_use:
        ngrok.set_auth_token(settings.ngrok_set_auth_token)
        public_url = ngrok.connect(8000).public_url
        print(public_url)
    uvicorn.run("kittens_store.app:app", reload=True)
