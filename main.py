from fastapi import FastAPI
from src.user import user_controller
from src.auth import auth_controller
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.background_jobs import remove_expired_user_accounts
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


scheduler = AsyncIOScheduler()

#start_date='2023-06-21 10:00:00'
scheduler.add_job(remove_expired_user_accounts, 'interval', seconds=10)
scheduler.start()

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    scheduler.shutdown()

@app.get("/")
async def root():
    return {"message": "Hello World!"}
