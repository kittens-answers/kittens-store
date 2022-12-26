from fastapi import APIRouter, Depends, Form, Request, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException


from kittens_store.data import data
from kittens_store.dependencies.init_data import InitData
from kittens_store.templates import templates
from kittens_store.bot.config import settings

router = APIRouter()


@router.get("/loader", response_class=HTMLResponse)
async def loader(request: Request):
    return templates.TemplateResponse("loader.html", {"request": request})


@router.post("/search", response_class=HTMLResponse)
async def menu(
    response: Response, request: Request, init_data: InitData = Depends(InitData)
):
    if init_data.is_valid is None:
        response.headers["HX-Redirect"] = settings.TG_BOT_URL
        return response
    if init_data.is_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return templates.TemplateResponse("search.html", {"request": request})


@router.post("/result", response_class=HTMLResponse)
async def test(
    response: Response,
    request: Request,
    q: str = Form(),
    init_data: InitData = Depends(InitData),
):
    if init_data.is_valid is None:
        response.headers["HX-Redirect"] = settings.TG_BOT_URL
        return response
    if init_data.is_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    questions = [qu for qu in data if q.lower() in qu.question.lower()]
    return templates.TemplateResponse(
        "item.html", {"request": request, "questions": questions}
    )
