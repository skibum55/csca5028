from typing import Optional
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED
# https://github.com/render-examples/fastapi/tree/main
# docs url will get you an OpenAPI/Swagger rendering

import dbAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/collect/{item_id}",status_code=HTTP_201_CREATED)
def read_item(item_id: str):
    dbAPI.create(item_id) 
    return {"q"}