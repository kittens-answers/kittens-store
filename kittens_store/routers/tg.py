from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from telegram import InlineQueryResultArticle, InputTextMessageContent

from kittens_store.bot import tg_bot
from kittens_store.data import data
from kittens_store.dependencies.init_data import InitData
from kittens_store.templates import templates

router = APIRouter()


@router.get("/search", response_class=HTMLResponse)
async def menu(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@router.post("/search", response_class=HTMLResponse)
async def test(request: Request, q: str = Form(), initData: str = Form(default="")):
    questions = [qu for qu in data if q.lower() in qu.question.lower()]
    return templates.TemplateResponse(
        "item.html", {"request": request, "questions": questions}
    )


@router.post("/close", response_class=HTMLResponse)
async def close(request: Request, q_id: str = Form()):
    return templates.TemplateResponse("close.html", {"request": request})


@router.get("/test-close")
async def test_close(request: Request, response: Response):
    response.headers["HX-Trigger"] = "closeTG"
    return "ok"


@router.post("/load")
async def load(
    request: Request, response: Response, init_data: InitData = Depends(InitData)
):
    # if init_data.is_valid is None:
    #     response.headers["HX-Redirect"] = settings.TG_BOT_URL
    #     return ""
    return templates.TemplateResponse("test.html", {"request": request})


@router.post("/test-answer")
async def test_answer(
    response: Response,
    init_data: InitData = Depends(InitData),
):
    response.headers["HX-Trigger"] = "closeTG"
    await tg_bot.answer_web_app_query(
        web_app_query_id=init_data.query_id,
        result=InlineQueryResultArticle(
            id="4",
            title="title",
            input_message_content=InputTextMessageContent(message_text="text"),
        ),
    )
