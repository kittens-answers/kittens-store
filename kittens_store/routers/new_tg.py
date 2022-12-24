from fastapi import APIRouter, Depends, Request
from telegram import InlineQueryResultArticle, InputTextMessageContent

from kittens_store.dependencies.init_data import InitData
from kittens_store.dependencies.tg_app import TGApp_Dep
from kittens_store.templates import templates

router = APIRouter()


@router.get("/menu")
async def menu(request: Request):
    print("menu")
    temp = templates.TemplateResponse("new-menu.html", {"request": request})
    print(temp.body.decode())
    return temp


@router.post("/click")
async def click(
    tg_app: TGApp_Dep = Depends(TGApp_Dep),
    init_data: InitData = Depends(InitData),
):
    print("click")
    print(init_data.data["query_id"])
    res = await tg_app.bot.answer_web_app_query(
        web_app_query_id=init_data.data["query_id"],
        result=InlineQueryResultArticle(
            id="4",
            title="title",
            input_message_content=InputTextMessageContent(message_text="text"),
        ),
    )
    print(res.inline_message_id)
