from fastapi import FastAPI
from telegram import Bot
from telegram.ext import ApplicationBuilder

from kittens_store.bot.commands import start
from kittens_store.bot.config import settings

tg_bot = Bot(token=settings.TG_TOKEN)
if settings.TG_TEST_MODE:
    tg_bot._base_url = tg_bot._base_url + "/test"
tg_app = ApplicationBuilder().bot(bot=tg_bot).updater(None).build()
tg_app.add_handler(start)


def init_tg_app(app: FastAPI):
    async def startup():
        await tg_app.initialize()
        await tg_app.bot.set_webhook(url=settings.webhook_url)

    async def shutdown():
        await tg_app.shutdown()

    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)
    app.state.tg_app = tg_app
