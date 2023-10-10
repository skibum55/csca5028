#!/usr/bin/env python3

from flask import Flask, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time
from components.metrics.prometheus import MetricsManager

app = Flask(__name__)

@app.route("/")
def main():
    start_time = time.time()
    # REQUEST_COUNT.labels('GET', '/', 200).inc()
    # REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
    return '''
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text

@app.route("/health")
def health():
    return {}

# https://github.com/prometheus/client_python
# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': MetricsManager.myMetrics()
})
