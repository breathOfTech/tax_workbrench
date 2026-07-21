.PHONY: start stop install dev test lint clean

# Start services
start:
	docker compose up -d
	.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Start chat UI (Chainlit)
chat:
	.venv/bin/chainlit run app/chat.py --port 8080

# Start only infrastructure (MongoDB, Redis)
infra:
	docker compose up -d

# Stop infrastructure
stop:
	docker compose down

# Install dependencies
install:
	pip install -e .

# Install with dev dependencies
dev:
	pip install -e ".[dev]"

# Run tests
test:
	pytest

# Lint
lint:
	ruff check .
	ruff format --check .

# Format
format:
	ruff check --fix .
	ruff format .

# Clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf dist build .pytest_cache
