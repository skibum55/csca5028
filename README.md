# Student Sentiment Analysis

## Executive Summary

As education moves away from mandatory classroom attendance, educators need to have a broader toolbox for fostering engagement.  Forums and chats provide an opportunity to gage the learners feelings about the course.  My product gives instructors, and their assistants, real-time insight into student sentiment.  This fast feedback encourages immediate adaptation in the case of misunderstandings while providing opportunities for future improvement.

## Initial Architecture Thoughts

![Diagram](./images/Mermaid-Product-Architecture.png)

## Quick Start

Install the prerequisites, initialize variables and create dedicated environment with ``` make install ```.  Be patient as there are a number of large data science libraries which need to load.

Run the application with ``` make run ```.  The homepage will be available here ->  [0.0.0.0:8000](http://0.0.0.0:8000). The first run will create a database and load a large public sentiment analysis model from [Hugging Face](https://huggingface.co/).

## TL;DR

Source code available at [Github](https://github.com/skibum55/csca5028) (minus credentials.)

db schema

``` make test ```
python3 -m pytest --ignore-glob=lib#####

front end

```flask --app applications/web/web.py run```

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000


data-collector

```uvicorn app.main:app```

```python3 -m applications.collector.slack```

docs

http://127.0.0.1:8000/docs#/ or /redoc

docker

```docker run -d -p 8000:8000 --env-file=.dockerenv csca5028:0.0.8```

https://github.com/UKPLab/sentence-transformers/issues/352

https://github.com/skibum55/csca5028/pkgs/container/csca5028


metrics


https://psychic-trout-ppq4r776r5hxg-8000.app.github.dev/metrics/

https://grafana.com/blog/2023/09/21/introducing-agentless-monitoring-for-prometheus-in-grafana-cloud/

https://seankeery.grafana.net/d/metrics-endpoint-overview/metrics-endpoint-overview?orgId=1&refresh=30s

Load Test = Integration

https://seankeery.grafana.net/a/k6-app/projects/3663881

### Stories Delivered
	
##### Web application basic form, reporting ❎

Report

##### Data collection ✅  

##### Data analyzer ✅

##### Unit tests ✅

##### Data persistence any data store ✅

##### Rest collaboration internal or API endpoint ✅

##### Product environment ✅ Venv, Render,[Github Codespaces](https://psychic-trout-ppq4r776r5hxg-8000.app.github.dev/)

##### Integration tests ✅✅

Makefile ✅

##### Continuous integration ✅✅ [Github Actions](https://github.com/skibum55/csca5028/actions)

##### Production monitoring instrumenting ✅✅ [Grafana Cloud](https://seankeery.grafana.net)

https://www.google.com/search?channel=fenc&client=firefox-b-1-lm&q=prometheus+requests+per+second

##### Continuous delivery ✅✅✅ [Render](https://dashboard.render.com) [Github Deploy Action](https://github.com/skibum55/csca5028/actions/runs/6525314861/job/17717874814)

##### Continuous security ✅✅✅✅

[Github Security](https://github.com/skibum55/csca5028/security)

![image](./images/continuous_security_overview.png)

![image2](./images/continuous_security_codeql.png)

### Backlog

##### Using mock objects or any test doubles ❎❎

##### Event collaboration messaging ❎❎❎

In this product, the data demands are low enough that we can do all our collection and analysis synchronously.  As Slack usage increases, it would make sense to modify our application to use a mq as shown in the architectural [diagram](#initial-architecture-thoughts).  A change to the Slack event driven [API](https://api.slack.com/events) would be better than scraping too.

#### Scheduler

As this is an MVP, scheduled collection wasn't a priority.  A _collection_ endpoint exists for triggering a manual collection.  Research indicates that this [FASTAPI Scheduler](https://pypi.org/project/fastapi-scheduler/) would be a good fit for adding this feature when needed.