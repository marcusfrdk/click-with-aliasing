.PHONY: venv install clean test lint format

# Variables
PYTHON := python3
VENV_DIR := .venv
SRC_DIR := click_with_aliasing
PIP := $(VENV_DIR)/bin/pip

# Environment
venv:
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment already exists at $(VENV_DIR)"; \
		echo "Run 'make clean' first if you want to recreate it"; \
	else \
		echo "Checking Python version..."; \
		$(PYTHON) --version | grep -qE "Python 3\.(1[0-9]|[2-9][0-9])" || \
			(echo "Error: Python 3.10 or higher is required" && exit 1); \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "Installing dependencies..."; \
		$(PIP) install --upgrade pip; \
		$(PIP) install -e ".[dev,build]"; \
		echo "Installation complete, activate the virtual environment with 'source $(VENV_DIR)/bin/activate'"; \
	fi

clean:
	rm -rf $(VENV_DIR) venv
	rm -rf *.egg-info
	rm -rf dist build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Testing
test:
	$(VENV_DIR)/bin/pytest tests/ -v

lint:
	$(VENV_DIR)/bin/pylint $(SRC_DIR) tests/

format:
	$(PYTHON) -m black $(SRC_DIR) tests/

type-check:
	$(PYTHON) -m mypy $(SRC_DIR) tests/

# Deploy
build:
	$(PYTHON) -m build