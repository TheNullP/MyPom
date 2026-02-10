from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from MyPom.routers import user, pomo, page
from fastapi.staticfiles import StaticFiles
from MyPom.core.config import templates


app = FastAPI()

# Routers
app.include_router(user.router, prefix="/user")
app.include_router(pomo.router, prefix="/pomo")
app.include_router(page.router, prefix="/page")

# Static Jinja2
app.mount("/static", StaticFiles(directory="MyPom/static"), name="static")
# Templates Jinja2


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )
