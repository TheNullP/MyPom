from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from MyPom.routers import user, pomo
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Routers
app.include_router(user.router)
app.include_router(pomo.router, prefix="/pomo")

# Static Jinja2
app.mount("/static", StaticFiles(directory="MyPom/static"), name="static")
# Templates Jinja2
templates = Jinja2Templates(directory="MyPom/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
        },
    )
