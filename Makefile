SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: help
help: ## Print this help message
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

.PHONY: init
init: ## Locally install all dev dependencies
	uv sync --all-extras

.PHONY: check
check: ## Run static checks
check: format lint typecheck

.PHONY: format
format: ## Format code
	uv run ruff format --target-version py312 --exit-non-zero-on-format

.PHONY: lint
lint: ## Lint code
	uv run ruff check --fix --show-fixes --exit-non-zero-on-fix

.PHONY: typecheck
typecheck: ## Check code types
	uv run ty check --error-on-warning

.PHONY: test
test: ## Run tests
	uv run pytest
