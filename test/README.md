# GraphReporter Tests

This directory contains tests for the GraphReporter application.

## Running Tests

You can run the tests using pytest:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=graphreporter

# Run specific test file
pytest test/test_auth_client.py

# Run tests with verbosity
pytest -v
```

## Test Structure

The tests are organized to match the package structure:

- `test_auth_client.py`: Tests for the authentication module
- `test_graph_client.py`: Tests for the base Graph client (to be implemented)
- `test_signins.py`: Tests for the sign-in logs client (to be implemented)
- `test_applications.py`: Tests for the applications client (to be implemented)
- `test_serviceprincipals.py`: Tests for the service principals client (to be implemented)
- `test_exporters/`: Tests for the export modules (to be implemented)
- `test_cli/`: Tests for the CLI interface (to be implemented)

## Mocking

Tests use the unittest.mock module to mock external dependencies like:

- MSAL library for authentication
- Requests library for API calls
- File system operations for exporters

This allows the tests to run without actual API credentials or external services.

## Test Data

Sample test data is stored in `test/data/` (to be implemented) and includes:

- Sample API responses
- Expected export outputs
- Test configurations

## Code Coverage

Aim for high code coverage (>80%) for all modules, with special attention to:

- Error handling
- Edge cases
- Configuration validation 