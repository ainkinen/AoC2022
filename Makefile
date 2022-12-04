.PHONY: all
all: lint type-check test
	@echo "All checks passed!"

.PHONY: install
install:
	poetry install --sync

.PHONY: test
test: install
	poetry run pytest

.PHONY: lint
lint: install
	poetry run flake8 .
	@echo "Linting OK!"

.PHONY: type-check
type-check: install
	poetry run mypy --check-untyped-defs --junit-xml='.mypy_cache/junit-report.xml' .
