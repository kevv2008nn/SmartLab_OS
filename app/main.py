from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.init_db import init_db

import app.auth.auth_router as auth
import app.routers.student as student
import app.routers.inventory as inventory
import app.dashboard.dashboard_router as dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="SmartLab OS",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(inventory.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "message": "SmartLab OS Running 🚀"
    }