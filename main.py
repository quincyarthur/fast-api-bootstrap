from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


@app.get("/")
async def root():
    return {"message": "Hello Quincy!"}
