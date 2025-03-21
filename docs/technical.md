# Technical Documentation

## Development Environment

### Python Version
- Python 3.8 or higher is required
- Virtual environment management with uv (recommended) or venv

### Development Tools
- Visual Studio Code with Python extensions recommended
- uv for dependency management and virtual environments
- Black for code formatting
- Isort for import sorting
- Flake8 for linting
- Pytest for testing

### Version Control
- Git for version control
- Conventional commits recommended for commit messages

## Technical Stack

### Core Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| msal | Microsoft Authentication Library for authentication | ^1.20.0 |
| requests | HTTP client for API requests | ^2.28.0 |
| pandas | Data manipulation and transformation | ^1.5.0 |
| typer | CLI interface | ^0.7.0 |
| pydantic | Data validation and settings management | ^1.10.0 |
| python-dotenv | Environment variable management | ^0.21.0 |
| openpyxl | Excel file generation | ^3.0.10 |
| rich | Rich terminal output | ^12.6.0 |

### Authentication
- Microsoft Authentication Library (MSAL) for Python
- Client credentials flow (application permissions)
- In-memory token caching
- No persistent storage of tokens

### API Integration
- Microsoft Graph API v1.0
- REST API calls using requests library
- JSON response parsing
- Pagination handling for large result sets

### Data Processing
- Pandas for data manipulation and transformation
- DataFrame operations for filtering and transformation
- Column selection and renaming for output customization

### Output Formats
- CSV using pandas' to_csv
- Excel using pandas with openpyxl
- JSON using built-in json module

## Application Configuration

### Configuration Sources
1. Command line arguments (highest priority)
2. Environment variables
3. Configuration file (.env)

### Required Configuration

| Setting | Environment Variable | Description |
|---------|----------------------|-------------|
| Tenant ID | GRAPH_TENANT_ID | Azure AD Tenant ID |
| Client ID | GRAPH_CLIENT_ID | Application (client) ID |
| Client Secret | GRAPH_CLIENT_SECRET | Client secret value |

### Optional Configuration

| Setting | Environment Variable | Default | Description |
|---------|----------------------|---------|-------------|
| Output Format | GRAPH_OUTPUT_FORMAT | csv | Default output format (csv, excel, json) |
| Output Directory | GRAPH_OUTPUT_DIR | ./output | Directory for output files |

## Development Workflow

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/graphreporter.git
cd graphreporter

# Using uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies with uv
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# Alternative: Using traditional venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running the Application

```bash
# Run the CLI
python -m graphreporter fetch-signins --last-days 7

# Get help
python -m graphreporter --help
```

### Development Build

```bash
# Install in development mode
pip install -e .
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=graphreporter
```

## API Endpoints

### Sign-in Logs
- Endpoint: `https://graph.microsoft.com/v1.0/auditLogs/signIns`
- Permission: `AuditLog.Read.All`
- Supports filtering by date, user, application, etc.

### Applications (App Registrations)
- Endpoint: `https://graph.microsoft.com/v1.0/applications`
- Permission: `Application.Read.All`
- Supports filtering and selection of specific properties

### Service Principals (Enterprise Apps)
- Endpoint: `https://graph.microsoft.com/v1.0/servicePrincipals`
- Permission: `Directory.Read.All`
- Supports filtering and selection of specific properties

## Authentication Flow

1. Create MSAL Confidential Client Application with client ID and secret
2. Acquire token for client with scopes `https://graph.microsoft.com/.default`
3. Use token in Authorization header for all Graph API requests
4. Handle token expiration and refresh as needed

## Error Handling

- HTTP errors are caught and displayed with appropriate context
- Authentication errors show helpful messages without exposing sensitive details
- API throttling is handled with exponential backoff
- Validation errors provide clear guidance on configuration issues

## Logging

- Structured logging using Python's logging module
- Different log levels (DEBUG, INFO, WARNING, ERROR)
- Console output for interactive use
- File logging for debugging and auditing

## Security Considerations

- Credentials are never logged
- Credentials are stored only in environment variables or secure configuration
- No persistent token storage
- Input validation for all user-provided parameters
- Output sanitization for exported data

## Performance Considerations

- Batch processing for large datasets
- Efficient pagination implementation
- Minimize memory usage for large result sets
- Optimize HTTP connections with session reuse
