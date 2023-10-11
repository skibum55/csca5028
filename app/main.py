from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
# https://github.com/render-examples/fastapi/tree/main
# docs url will get you an OpenAPI/Swagger rendering

import db.dbAPI as db
import app.collector.slack as slack
import app.analyzer.sentiment as sentiment
from components.metrics.prometheus import MetricsManager, REQUEST_COUNT, REQUEST_LATENCY, REQUEST_TIME
import time

# initialize app
app = FastAPI()

# https://stackoverflow.com/questions/65296604/how-to-return-a-htmlresponse-with-fastapi
@app.get("/", response_class=HTMLResponse)
async def main():
    start_time = time.time()
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    # https://plotly.com/javascript/gauge-charts/
    html_content = """<head>
	<!-- Load plotly.js into the DOM -->
	<script src='https://cdn.plot.ly/plotly-2.26.0.min.js'></script>
</head>

<body>
	<div id='speedometerDiv'><!-- Plotly speedometer will be drawn inside this DIV --></div>
    <div id='chartDiv'><!-- Plotly chart will be drawn inside this DIV --></div>
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
        x: [1, 2, 3, 4],
        y: [0, 2, 3, 5],
        fill: 'tozeroy',
        type: 'scatter',
        line: {shape: 'spline'}
        };

        var trace2 = {
        x: [1, 2, 3, 4],
        y: [3, 5, 1, 7],
        fill: 'tonexty',
        type: 'scatter',
        line: {shape: 'spline'}
        
        };

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
    return HTMLResponse(content="OK", status_code=200)

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

@app.get("/analyze/{sentence}",status_code=HTTP_201_CREATED)
def analyze_data(sentence: str):
    q=sentiment.sentimentAnalyzer(sentence) 
    return HTMLResponse(q.labels[0].value,status_code=201)

@app.get("/db/{dbname}",status_code=HTTP_201_CREATED)
def read_item(dbname: str):
    db.create(dbname) 
    return dbname

# https://github.com/prometheus/client_python
metrics_app = MetricsManager.myMetrics()
app.mount("/metrics", metrics_app)

# TODO - add scheduler https://pypi.org/project/fastapi-scheduler/