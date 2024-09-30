# Makefile for Python project

# Variables
PYTHON = python3
PIP = pip
TEST_DIR = tests
DOCS_DIR = docs

# Targets
.PHONY: help install clean test lint docs

# Help
help:
 @echo "Makefile commands:"
 @echo "  install   - Install dependencies"
 @echo "  clean     - Remove temporary files and directories"
 @echo "  test      - Run tests"
 @echo "  lint      - Run linters"
 @echo "  docs      - Build documentation"

# Install dependencies
install:
 $(PIP) install -r requirements.txt
 $(PIP) install -r requirements-dev.txt

# Clean temporary files
clean:
 rm -rf pycache/
 find . -name "*.pyc" -delete

# Run tests
test:
 $(PYTHON) -m unittest discover -s $(TEST_DIR)

# Run linters (e.g., flake8, mypy)
lint:
 flake8 .
 mypy .

# Build documentation
docs:
 $(PYTHON) -m sphinx $(DOCS_DIR) docs/_build