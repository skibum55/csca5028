from typing import Optional
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED
# https://github.com/render-examples/fastapi/tree/main
# docs url will get you an OpenAPI/Swagger rendering

import db.dbAPI as dbAPI
import app.collector.slack as slack

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/collect/",status_code=HTTP_201_CREATED)
def collect_data():
    q=slack.myfunction() 
    return q

@app.get("/db/{dbname}",status_code=HTTP_201_CREATED)
def read_item(dbname: str):
    dbAPI.create(dbname) 
    return dbname