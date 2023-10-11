# https://earthly.dev/blog/python-makefile/
run:
    python app.py
    flask run
    uvicorn app.main:app 
clean:
    rm -rf __pycache__

env:
	source .env

init:
    pip install -r requirements.txt

test:
    pip install -r test/requirements.txt
    py.test tests
    python3 -m unittest

.PHONY: init test