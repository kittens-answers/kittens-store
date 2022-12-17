import logging
from telegram import Update, Bot, MenuButtonWebApp, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from fastapi import FastAPI

from kittens_store.bot.config import settings

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_app(test_mode: bool = False):
    bot = Bot(token=settings.TG_TOKEN)
    if test_mode:
        bot._base_url = bot._base_url + "/test"
    app = ApplicationBuilder().bot(bot=bot).updater(None).build()
    return app


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("start")
    assert update.effective_chat
    await context.bot.setChatMenuButton(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(
            text="menu", web_app=WebAppInfo(url=settings.urls.menu)
        ),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


class TG_App:
    def __init__(self) -> None:
        self.tg_app = get_app(test_mode=True)
        self.tg_app.add_handler(CommandHandler("start", start))

    async def init(self):
        res = await self.tg_app.bot.set_webhook(
            url=f"https://store.kittensanswers.ru/tg/{settings.TG_TOKEN}"
        )
        print(f"web hook set: {res}")


def init_tg_app(app: FastAPI):
    tg_app = TG_App()
    app.add_event_handler("startup", tg_app.init)
