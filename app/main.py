from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.init_db import init_db

import app.auth.auth_router as auth
import app.routers.student as student
import app.routers.inventory as inventory
import app.dashboard.dashboard_router as dashboard
import app.attendance.router as attendance
import app.lab_sessions.router as lab_session
import app.borrow_return.router as borrow


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
app.include_router(attendance.router)
app.include_router(lab_session.router)
app.include_router(borrow.router)


@app.get("/")
def root():
    return {
        "message": "SmartLab OS Running 🚀"
    }