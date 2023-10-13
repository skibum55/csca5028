"""Function providing prometheus scrape endpoint."""
from prometheus_client import make_asgi_app, Counter, Histogram, Summary


# https://medium.com/@letathenasleep/exposing-python-metrics-with-prometheus-c5c837c21e4d
REQUEST_COUNT = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Application Request Latency',
    ['method', 'endpoint']
)

REQUEST_TIME = Summary(
    'request_processing_seconds', 
    'Time spent processing request')

"""Function printing python version."""
class MetricsManager():
    """Function printing python version."""
    def mymetrics(self):
        """Function printing python version."""
        return make_asgi_app()
