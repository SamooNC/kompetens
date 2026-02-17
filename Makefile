.PHONY: up down dev-api dev-web test test-api test-web lint format db-migrate db-seed import-rome import-opendata collect-offers build-referentiel audit-anon

# --- Docker ---
up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

# --- Development (local, outside Docker) ---
dev-api:
	cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-web:
	cd apps/web && npx vite --host 0.0.0.0

# --- Testing ---
test: test-api test-web

test-api:
	cd apps/api && python -m pytest -v

test-web:
	cd apps/web && npx vitest run

# --- Code quality ---
lint:
	ruff check apps/api scripts
	cd apps/web && npx eslint src/

format:
	ruff format apps/api scripts
	cd apps/web && npx prettier --write src/

# --- Database ---
db-migrate:
	cd apps/api && alembic upgrade head

db-seed:
	cd apps/api && python -m scripts.seed

# --- Data import ---
import-rome:
	python scripts/import_rome.py

import-opendata:
	python scripts/import_opendata.py

# --- Referentiel emergent ---
collect-offers:
	python scripts/collect_offers.py

build-referentiel:
	python scripts/build_referentiel.py

# --- Audit ---
audit-anon:
	cd apps/api && python -m pytest tests/test_anonymisation.py -v
