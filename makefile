# https://earthly.dev/blog/python-makefile/
run:
    python app.py
    flask run
clean:
    rm -rf __pycache__

env:
	source .env

init:
    pip install -r requirements.txt

test:
    py.test tests

.PHONY: init test