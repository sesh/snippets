test:
  uv run --with=thttp python -m unittest cached_get/cached_get.py

format:
  uvx black .

bandit:
  uvx bandit -r .

all: test format bandit
