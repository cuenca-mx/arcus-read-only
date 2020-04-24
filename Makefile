SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON = python3.7
PROJECT = arcus-read-only
isort = isort -rc -ac chalicelib tests app.py
black = black -S -l 79 --target-version py37 chalicelib tests app.py

all: test

default: install

venv:
	$(PYTHON) -m venv --prompt $(PROJECT) venv
	pip install -qU pip

install:
	pip install -qU -r requirements.txt

install-dev: install
	pip install -q -r requirements-dev.txt

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test: clean-pyc lint
	pytest --cov-report term-missing tests/ --cov=. --cov-config=.coveragerc

format:
	$(isort)
	$(black)

lint:
	$(isort) --check-only
	$(black) --check
	flake8 chalicelib tests app.py
	mypy chalicelib tests app.py

serve:
	chalice local

deploy:
	chalice deploy --stage development --profile development

deploy-prod:
	chalice deploy --stage production --profile production

destroy:
	chalice delete --stage development --profile development

destroy-prod:
	chalice delete --stage production --profile production

.PHONY: install install-dev lint clean-pyc test