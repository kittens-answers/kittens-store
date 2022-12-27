from telegram import MenuButtonWebApp, Update, WebAppInfo
from telegram.ext import CommandHandler, ContextTypes

from kittens_store.bot.config import settings


async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_chat
    await context.bot.setChatMenuButton(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(
            text="Меню", web_app=WebAppInfo(url=settings.load_url)
        ),
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Для поиска открой меню"
    )


start = CommandHandler("start", _start)
