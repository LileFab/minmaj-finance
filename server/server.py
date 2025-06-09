from typing import Union
from db.init_db import init_db

from fastapi import FastAPI
from api import router as api_router

app = FastAPI()
app.include_router(api_router)

init_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}
