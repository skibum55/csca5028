# https://earthly.dev/blog/python-makefile/
run:
    python app.py
setup: requirements.txt
    pip install -r requirements.txt
clean:
    rm -rf __pycache__
env:
	source env