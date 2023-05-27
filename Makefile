PORT ?= 8000

install:
	poetry install -vvv

build: check
	poetry build

dev:
	poetry run flask --app page_analyzer:app --debug run

start:
	poetry run gunicorn --workers=5 --bind=0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer
	poetry run black page_analyzer --diff

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

check:
	poetry check

db-create:
	createdb page_analyzer || echo 'skip'

schema-load:
	psql page_analyzer < database.sql

connect:
	psql page_analyzer

all-checks: check lint

database: db-create schema-load

.PHONY: install all-checks build
