from dataclasses import dataclass

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from kittens_store.templates import templates
from kittens_store.data import data
router = APIRouter()


@router.get("/search", response_class=HTMLResponse)
async def menu(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@router.post("/search", response_class=HTMLResponse)
async def test(request: Request, q: str = Form(), initData: str = Form(default="")):
    questions = [qu for qu in data if q in qu.question]
    return templates.TemplateResponse(
        "item.html", {"request": request, "questions": questions}
    )


@router.post("/close", response_class=HTMLResponse)
async def close(request: Request, q_id: str = Form()):
    print(q_id)
    return templates.TemplateResponse("close.html", {"request": request})
