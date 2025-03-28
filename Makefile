include .env

export OPENAI_API_KEY := $(OPENAI_API_KEY)

test:
	PYTHONPATH=src uv run pytest -s tests
lint:
	uv run isort src tests
	uv run black -l 79 src tests
	uv run flake8 src tests
