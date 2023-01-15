from fastapi import FastAPI
from db.config import engine, Base
from src.user import user_controller
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_HOSTS = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_controller.router)

import debugpy

debugpy.listen(("0.0.0.0", 5678))


async def create_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    await create_schema()
    return {"message": "Hello World!"}
