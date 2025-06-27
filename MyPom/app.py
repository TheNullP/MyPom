from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import user


app = FastAPI()

# Routers
app.include_router(user.router)


@app.get("/")
def root():
    return JSONResponse(
        content={"msg": "Hello World!"},
        status_code=200,
    )
