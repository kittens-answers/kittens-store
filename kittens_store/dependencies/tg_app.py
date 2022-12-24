from fastapi import Request

from kittens_store.bot import TG_App


class TGApp_Dep:
    def __init__(self, request: Request) -> None:
        self.tg_app: TG_App = request.app.state.tg_app
        self.bot = self.tg_app.tg_app.bot
