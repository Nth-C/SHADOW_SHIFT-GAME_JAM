PYTHON = .venv/bin/python

lint-fix: 
	ruff check --fix

format:
	ruff format

lint-format: 
	ruff check --fix && ruff format

start:
	python src/main.py