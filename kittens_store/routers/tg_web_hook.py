from fastapi import APIRouter, Request
from telegram import Update

from kittens_store.bot import tg_app
from kittens_store.bot.config import settings

router = APIRouter()


@router.post(f"/{settings.TG_TOKEN}", include_in_schema=False)
async def update(request: Request):
    json = await request.json()
    await tg_app.process_update(Update.de_json(data=json, bot=tg_app.bot))
