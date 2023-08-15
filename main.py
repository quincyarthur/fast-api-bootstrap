from fastapi import FastAPI
from src.user import user_controller
from src.auth import auth_controller
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import asyncio
import aio_pika
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


@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    connection = await aio_pika.connect("amqp://guest:guest@localhost/", loop=loop)
    channel = await connection.channel()
    not_activated_queue = await channel.declare_queue("not-activated")
    await not_activated_queue.consume()


my_cron = CronTab(user="root")
job_add_non_activated_accounts = my_cron.new(
    command="python /app/src/background_jobs/add_non_activated_accounts.py"
)
job_add_non_activated_accounts.hour.every(1)
my_cron.write()


@app.get("/")
async def root():
    return {"message": "Hello World!"}
