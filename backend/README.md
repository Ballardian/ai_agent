# Backend

This is the backend service for the AI Agent project. It provides core functionality for processing and managing AI-related tasks.

## Project Structure

```
backend/
├── src/                    # Source code directory
│   └── backend/           # Main package directory
├── tests/                 # Test files
├── utils/                 # Utility functions and helpers
├── pyproject.toml         # Poetry project configuration
└── poetry.lock           # Poetry dependency lock file
```

## Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)

## Installation

1. Install Poetry if you haven't already:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository and navigate to the backend directory:

   ```bash
   cd backend
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

## Virtual Environment

Poetry automatically creates and manages a virtual environment for your project. Here's how to work with it:

### Activate the virtual environment

```bash
poetry shell
```

### Run commands within the virtual environment (without activating)

```bash
poetry run <command>
```

## Development

### Running Tests

The project uses pytest for testing. To run tests:

```bash
# Run all tests
poetry run pytest

# Run tests with coverage report
poetry run pytest --cov=backend

# Run specific test file
poetry run pytest tests/<test_file>.py

# Run tests with verbose output
poetry run pytest -v
```

### Adding New Dependencies

To add a new dependency:

```bash
poetry add <package-name>
```

For development dependencies:

```bash
poetry add --group dev <package-name>
```

### Updating Dependencies

To update all dependencies:

```bash
poetry update
```

To update a specific package:

```bash
poetry update <package-name>
```
