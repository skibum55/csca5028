from typing import Optional
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED
# https://github.com/render-examples/fastapi/tree/main
# docs url will get you an OpenAPI/Swagger rendering

import db.dbAPI as dbAPI
import app.collector.slack as slack
from components.metrics.prometheus import MetricsManager
import time

app = FastAPI()

@app.get("/")
async def main():
    start_time = time.time()
    # REQUEST_COUNT.labels('GET', '/', 200).inc()
    # REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    return 'Hola Mundo!'

# @app.post("/echo_user_input")
# async def echo_input(user_input: Annotated[str, Form()]):
#     return "You entered: " + user_input

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

# https://github.com/prometheus/client_python
metrics_app = MetricsManager.myMetrics()
app.mount("/metrics", metrics_app)