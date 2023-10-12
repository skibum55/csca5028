FROM python:3.10.13-slim-bookworm

WORKDIR /csca5028

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD https://nlp.informatik.hu-berlin.de/resources/models/sentiment-curated-distilbert/sentiment-en-mix-distillbert_4.pt .
RUN mkdir -p /root/.flair/models && mv sentiment-en-mix-distillbert_4.pt /root/.flair/models/sentiment-en-mix-distillbert_4.pt
COPY . .

EXPOSE 8000
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port 8000