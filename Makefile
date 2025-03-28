include .env

export OPENAI_API_KEY := $(OPENAI_API_KEY)

test:
	PYTHONPATH=src uv run pytest -s tests
