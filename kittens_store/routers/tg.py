from fastapi import APIRouter, Form, Request, Depends, Response
from fastapi.responses import HTMLResponse

from kittens_store.data import data
from kittens_store.templates import templates
from kittens_store.bot.config import settings
from kittens_store.bot import TG_App
from kittens_store.dependency import tg_depend
from telegram import Update

router = APIRouter()


@router.post(f"/{settings.TG_TOKEN}", include_in_schema=False)
async def update(request: Request, tg: TG_App = Depends(tg_depend)):
    json = await request.json()
    await tg.tg_app.process_update(Update.de_json(data=json, bot=tg.tg_app.bot))
    return "ok"


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
