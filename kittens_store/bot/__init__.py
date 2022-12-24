import logging

from fastapi import FastAPI
from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Update,
    WebAppInfo,
)
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
    assert update.effective_chat
    await context.bot.setChatMenuButton(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(
            text="menu", web_app=WebAppInfo(url=settings.search_url)
        ),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def new_tg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_chat
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="new",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text="open", web_app=WebAppInfo(url=""))
        ),
    )


class TG_App:
    def __init__(self) -> None:
        self.tg_app = get_app(test_mode=settings.TG_TEST_MODE)
        self.tg_app.add_handler(CommandHandler("start", start))
        self.tg_app.add_handler(CommandHandler("new", new_tg))

    async def startup(self):
        await self.tg_app.initialize()
        res = await self.tg_app.bot.set_webhook(url=settings.webhook_url)
        print(f"web hook set: {res}")

    async def shutdown(self):
        await self.tg_app.shutdown()


def init_tg_app(app: FastAPI):
    tg_app = TG_App()
    app.add_event_handler("startup", tg_app.startup)
    app.add_event_handler("shutdown", tg_app.shutdown)
    app.state.tg_app = tg_app
