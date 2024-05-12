from typing import Any
from dotenv import load_dotenv

from routers import posts, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app: Any = FastAPI(title="Fastapi backend for blog")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
