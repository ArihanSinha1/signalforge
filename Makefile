SHELL := /bin/bash

.PHONY: up down logs api web db migrate seed test

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

api:
	docker compose exec api bash

web:
	docker compose exec web sh

db:
	docker compose exec db psql -U sgf_user -d signalforge

migrate:
	docker compose exec api alembic upgrade head

seed:
	docker compose exec api python -m app.seed || docker compose exec api python app/seed.py

test:
	docker compose exec api pytest -q

make-up:
	$(MAKE) up

make-down:
	$(MAKE) down

make-migrate:
	$(MAKE) migrate

make-seed:
	$(MAKE) seed

make-test:
	$(MAKE) test
