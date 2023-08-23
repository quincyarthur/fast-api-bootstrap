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


with CronTab(user="root") as my_cron:
    if not list(my_cron.find_comment(comment="job_remove_expired_user_accounts")):
        job_remove_expired_user_accounts = my_cron.new(
            command="/app/src/background_jobs/set_env.sh /usr/local/bin/python /app/src/background_jobs/remove_expired_user_accounts.py",
            comment="job_remove_expired_user_accounts",
        ).minute.every(1)
    my_cron.write()


@app.get("/")
async def root():
    return {"message": "Hello World!"}
