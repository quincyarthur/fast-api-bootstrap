from fastapi import FastAPI
from db.config import engine, Base
import os
from src.user import user_controller

app = FastAPI()

app.include_router(user_controller.router)


async def create_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    await create_schema()
    return {"message": "Hello Quincy!"}
