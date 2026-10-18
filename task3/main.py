from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from lcm import count_lcm
from local_config import EMAIL_PATH

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "Hello"

@app.get(f"/{EMAIL_PATH}", response_class=PlainTextResponse)
def get_lcm(x: str, y: str):
    return count_lcm(x, y)
