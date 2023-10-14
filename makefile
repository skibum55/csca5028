SHELL = /usr/bin/env bash -o pipefail
# https://earthly.dev/blog/python-makefile/
# https://stackoverflow.com/questions/33839018/activate-virtualenv-in-makefile

default: install

all: install run

.PHONY: install test run

install: venv
    # Activate venv and install smthing inside
	. venv/bin/activate pip install -r requirements.txt
	. .env
    # Other commands here

venv:
    # Create venv if it doesn't exist
    # test -d venv || virtualenv -p python3 --no-site-packages venv
	test -d venv || python3 -m venv venv

run: venv
	source venv/bin/activate; \
	. .env; \
	uvicorn --host "0.0.0.0" app.main:app

clean:
	rm -rf __pycache__
	rm *.db

test: venv
	source venv/bin/activate; \
	. .env; \
	python3 -m pytest; \