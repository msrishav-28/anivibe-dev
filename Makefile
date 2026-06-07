# AniVibe Makefile

.PHONY: help install dev test lint format clean docker-build docker-up docker-down docker-logs migrate db-setup embeddings-smoke local-smoke visual-eval start stop restart dev-setup deploy

help:
	@echo "AniVibe - Makefile Commands"
	@echo "======================================"
	@echo "install        - Install development dependencies"
	@echo "dev            - Run development server"
	@echo "test           - Run tests"
	@echo "lint           - Run linting"
	@echo "format         - Format code"
	@echo "clean          - Clean cache and build files"
	@echo "docker-build   - Build Docker images"
	@echo "docker-up      - Start Docker services"
	@echo "docker-down    - Stop Docker services"
	@echo "migrate        - Run database migrations"
	@echo "db-setup       - Import the 250-anime MAL/Jikan smoke dataset"
	@echo "embeddings-smoke - Generate local SBERT embeddings for the smoke dataset"
	@echo "local-smoke    - Run API smoke checks against a running local backend"
	@echo "visual-eval    - Run local poster visual-search evaluation"

install:
	pip install -r requirements-dev.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --cov=app --cov-report=term-missing

lint:
	ruff check app tests
	mypy app/

format:
	ruff format app tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "Services started."
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

migrate:
	alembic upgrade head

db-setup:
	python scripts/fetch_mal_data.py --limit 250 --import-db

embeddings-smoke:
	python scripts/generate_embeddings.py --batch-size 16

local-smoke:
	python scripts/local_product_smoke.py

visual-eval:
	python scripts/evaluate_visual_search.py --limit 250 --generate --evaluate

start: docker-up
	@echo "AniVibe is running."

stop: docker-down
	@echo "AniVibe stopped."

restart: stop start
	@echo "AniVibe restarted."

dev-setup: install db-setup
	@echo "Development environment ready."

deploy:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.prod.yml up -d --build
