PORT ?= 8000

install:
	poetry install

build: check
	poetry build

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

selfcheck:
	poetry check

check: selfcheck lint

.PHONY: install check build
