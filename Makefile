include .env

export OPENAI_API_KEY := $(OPENAI_API_KEY)

run:
	PYTHONPATH=src uv run python -m pocket_researcher.main

test:
	PYTHONPATH=src uv run pytest -s tests
lint:
	uv run isort src tests
	uv run black -l 79 src tests
	uv run flake8 src tests
