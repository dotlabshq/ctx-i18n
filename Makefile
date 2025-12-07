.PHONY: build

build-env:
	python3 -m venv .venv
	.venv/bin/pip install poetry
	.venv/bin/poetry install

build:
	.venv/bin/poetry build

test:
	.venv/bin/poetry run pytest