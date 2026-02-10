from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from starlette.responses import RedirectResponse

from app.database import Base, engine
from app.routers import users, auth

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="secret123")

Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return RedirectResponse("/login")