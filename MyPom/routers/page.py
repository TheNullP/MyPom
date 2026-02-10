from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from MyPom.core.config import templates


router = APIRouter(tags=["pages"])


@router.get("/report", response_class=HTMLResponse)
async def report(request: Request):
    return templates.TemplateResponse(
        "report.html",
        {"request": request},
    )
