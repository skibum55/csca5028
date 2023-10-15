"""Module providing fastapi routing function."""
from typing import Optional
import os
import time
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
import uvicorn
# https://github.com/render-examples/fastapi/tree/main
# docs url will get you an OpenAPI/Swagger rendering
from components.metrics.prometheus import MetricsManager, REQUEST_COUNT, REQUEST_LATENCY
#, REQUEST_TIME

import db.db_api as db
from app.collector import slack
from app.analyzer import sentiment


# initialize app
app = FastAPI()
db_filename = os.environ.get("SQLITE_DB")
db.create(db_filename)
slack.slack_collect()

def get_plot_values(tag,key):
    """function to get trace values"""
    # ["2023-07-18","2023-08-16","2023-08-17"] format example
    myplot =[]
    plotrows = db.get_daily_sentiment(tag)
    for row in plotrows:
        d = json.dumps(row[key])
        myplot.append(d)
    return str(myplot)


# https://stackoverflow.com/questions/65296604/how-to-return-a-htmlresponse-with-fastapi
@app.get("/", response_class=HTMLResponse)
async def main():
    """Function to load homepage."""
    start_time = time.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    # REQUEST_TIME.labels('GET','/').observe(time.time() - start_time)
    # https://plotly.com/javascript/gauge-charts/
    html_content = """<head>
	<!-- Load plotly.js into the DOM -->
	<script src='https://cdn.plot.ly/plotly-2.26.0.min.js'></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js'></script>
</head>

<body>
    <h1>Current Sentiment</h1>
    <p>
	<div id='speedometerDiv', width=250px, height=250px><!-- Plotly speedometer will be drawn inside this DIV --></div>
    <h1>Sentiment Over Time</h1>
    <div id='chartDiv'><!-- Plotly timeseries will be drawn inside this DIV --></div>
    <script>
    // JavaScript Code
        var data = [
        {
            type: "indicator",
            mode: "gauge+number+delta",
            value: """ + db.get_average_sentiment() +""",
            title: { text: "sentiment", font: { size: 24 } },
            delta: { reference: 450, increasing: { color: "RebeccaPurple" } },
            gauge: {
            axis: { range: [-1, 1], tickwidth: .25, tickcolor: "darkblue" },
            bar: { color: "darkblue" },
            bgcolor: "white",
            borderwidth: 2,
            bordercolor: "gray",
            steps: [
                { range: [-2, -.5], color: "red" },
                { range: [-.5, .5], color: "yellow" },
                { range: [.5, 1], color: "green"}
            ],
            threshold: {
                line: { color: "red", width: 4 },
                thickness: 0.75,
                value: 0.75
            }
            }
        }
        ];
        var layout = {
        width: 500,
        height: 400,
        margin: { t: 25, r: 25, l: 25, b: 25 },
        paper_bgcolor: "lavender",
        font: { color: "darkblue", family: "Arial" }
        };
        Plotly.newPlot('speedometerDiv', data, layout);
        // https://plotly.com/javascript/time-series/
var trace1 = {
  type: "scatter",
  mode: "lines",
  name: 'POSITIVE',
  x: """ + get_plot_values("POSITIVE","day")+ """,
  y: """ + get_plot_values("POSITIVE","count")+ """,
  line: {color: '#17BECF'},
  line: {shape: 'spline'},
  fill: 'tonexty'
}

var trace2 = {
  type: "scatter",
  mode: "lines",
  name: 'NEGATIVE',
    x: """ + get_plot_values("POSITIVE","day")+ """,
    y: """ + get_plot_values("NEGATIVE","count")+ """,
  line: {color: '#f04030'},
  line: {shape: 'spline'},
  fill: 'tozeroy',
}
        var data = [trace1, trace2];

        Plotly.newPlot('chartDiv', data);

    </script>
</body>"""
    # https://fastapi.tiangolo.com/advanced/custom-response/
    return HTMLResponse(content=html_content, status_code=200)

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=HTTP_200_OK
)
def healthcheck():
    """Function returning liveness info."""
    return HTMLResponse(content="OK", status_code=200)

# @app.post("/echo_user_input")
# async def echo_input(user_input: Annotated[str, Form()]):
#     return "You entered: " + user_input

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     """Function printing python version."""
#     return {"item_id": item_id, "q": q}

@app.get("/collect/",status_code=HTTP_201_CREATED)
def collect_data():
    """Function to collect data."""
    q=slack.slack_collect()
    return q

@app.get("/analyze/{sentence}",status_code=HTTP_201_CREATED)
def analyze_data(sentence: str):
    """Function to analyze sentence."""
    q=sentiment.sentiment_analyzer(sentence)
    return HTMLResponse(q.labels[0].value,status_code=201)

@app.get("/db/{dbname}",status_code=HTTP_201_CREATED)
def read_db(dbname: str):
    """Function to create db."""
    db.create(dbname)
    return dbname

# https://github.com/prometheus/client_python
metrics_app = MetricsManager.mymetrics('')
app.mount("/metrics", metrics_app)

# TODO - add scheduler https://pypi.org/project/fastapi-scheduler/

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
