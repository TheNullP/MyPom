from fastapi import FastAPI
from fastapi.responses import JSONResponse
from MyPom.routers import user, pomo


app = FastAPI()

# Routers
app.include_router(user.router)
app.include_router(pomo.router)


@app.get("/")
def root():
    return JSONResponse(
        content={"msg": "Hello World!"},
        status_code=200,
    )
