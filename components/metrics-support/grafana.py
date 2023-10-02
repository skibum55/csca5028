
import requests
import base64

GRAFANA_USER_ID = os.environ.get("GRAFANA_USER_ID", "")
GRAFANA_API_KEY = os.environ.get("GRAFANA_API_KEY", "")
body = 'test,bar_label=abc,source=grafana_cloud_docs metric=35.2'

response = requests.post('https://influx-prod-36-prod-us-west-0.grafana.net/api/v1/push/influx/write', 
                         headers = {
                           'Content-Type': 'text/plain',
                         },
                         data = str(body),
                         auth = (GRAFANA_USER_ID, GRAFANA_API_KEY)
)

status_code = response.status_code

print(status_code)