from fastapi import FastAPI
from src.user import user_controller
from src.auth import auth_controller
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from crontab import CronTab

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


my_cron = CronTab(user="root")
job_add_non_activated_accounts = my_cron.new(
    command="python /app/src/background_jobs/remove_expired_user_accounts.py"
)
job_add_non_activated_accounts.hour.every(1)
my_cron.write()


@app.get("/")
async def root():
    return {"message": "Hello World!"}
