from fastapi import FastAPI
from src.user import user_controller
from src.auth import auth_controller
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.engine import create_engine
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from src.background_jobs.remove_expired_user_accounts import (
    sync_remove_expired_accounts,
)
from datetime import datetime
import os
from alembic.config import Config
from alembic.command import upgrade

ALLOWED_HOSTS = ["*"]

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="secret-string")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_controller.router)
app.include_router(auth_controller.router)


data_store = SQLAlchemyJobStore(
    engine=create_engine(
        url=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
)
scheduler = BackgroundScheduler(timezone="UTC")
scheduler.configure(
    jobstores={"default": data_store},
    job_defaults={"coalesce": True, "max_instances": 1},
)

try:
    scheduler.add_job(
        sync_remove_expired_accounts,
        "interval",
        hours=24,
        start_date=datetime.combine(datetime.utcnow(), datetime.min.time()),
        misfire_grace_time=(12 * 60 * 60),
    )
    scheduler.start()
except KeyboardInterrupt:
    pass
finally:
    scheduler.shutdown()


@app.on_event("startup")
async def startup() -> None:
    upgrade(Config(), "head")


@app.get("/")
async def root():
    return {"message": "Hello World!"}
