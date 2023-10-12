FROM python:slim

WORKDIR /csca5028

COPY . /csca5028/
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "/csca5028/app.main:app" ]