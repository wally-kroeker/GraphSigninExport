# GraphReporter

A Python CLI tool for retrieving and reporting Microsoft Entra ID (Azure AD) data using Microsoft Graph API.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

GraphReporter is a command-line tool that helps IT administrators and security professionals extract and analyze data from Microsoft Entra ID (Azure AD). It uses the Microsoft Graph API to retrieve sign-in logs, app registrations, and enterprise applications, and exports this data in various formats for analysis.

### Features

- **Authentication**: Secure client credentials (app-only) authentication with Microsoft Graph API
- **Data Retrieval**: Fetch sign-in logs, app registrations, and enterprise apps
- **Filtering**: Filter data by date, type, and other properties
- **Export**: Export data to CSV, Excel, or JSON formats
- **Pagination**: Handle large datasets with proper pagination

## Prerequisites

Before using GraphReporter, you need to:

1. Register an application in Microsoft Entra ID (Azure AD)
2. Grant the following API permissions:
   - AuditLog.Read.All (Application)
   - Directory.Read.All (Application)
   - Application.Read.All (Application)
3. Generate a client secret

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/graphreporter.git
cd graphreporter

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Configuration

GraphReporter requires the following configuration:

1. Create a `.env` file in the project root with your Azure AD details:

```
GRAPH_TENANT_ID=your-tenant-id
GRAPH_CLIENT_ID=your-client-id
GRAPH_CLIENT_SECRET=your-client-secret
```

Or set these environment variables manually:

```bash
export GRAPH_TENANT_ID=your-tenant-id
export GRAPH_CLIENT_ID=your-client-id
export GRAPH_CLIENT_SECRET=your-client-secret
```

## Usage

### Fetch Sign-In Logs

```bash
# Fetch sign-in logs for the last 7 days in CSV format
python -m graphreporter fetch-signins --last-days 7 --format csv

# Fetch sign-in logs within a specific date range in Excel format
python -m graphreporter fetch-signins --start-date 2023-01-01 --end-date 2023-01-31 --format excel

# Fetch sign-in logs and filter by specific user
python -m graphreporter fetch-signins --last-days 30 --user-id user@example.com
```

### List App Registrations

```bash
# List all app registrations in CSV format
python -m graphreporter list-apps --format csv

# List app registrations with specific permissions
python -m graphreporter list-apps --permission "Mail.Read"
```

### List Enterprise Applications

```bash
# List all enterprise apps in CSV format
python -m graphreporter list-service-principals --format csv

# List recently added enterprise apps
python -m graphreporter list-service-principals --created-after 2023-01-01
```

### General Options

```bash
# Get help
python -m graphreporter --help

# Get help for a specific command
python -m graphreporter fetch-signins --help

# Specify output directory
python -m graphreporter fetch-signins --last-days 7 --output-dir ./reports
```

## Output Examples

### Sign-In Logs CSV Example

```
id,createdDateTime,userPrincipalName,appDisplayName,ipAddress,clientAppUsed,status
01234567-89ab-cdef-0123-456789abcdef,2023-01-15T14:32:16Z,user@example.com,Microsoft Office,203.0.113.1,Mobile Apps and Desktop clients,success
```

### App Registrations Excel Example

The Excel output includes:
- App ID
- Display Name
- App Permissions
- Granted Permissions
- Creation Date
- Owner Information

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/graphreporter.git
cd graphreporter

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=graphreporter
```

## Project Structure

```
graphreporter/
├── cli/                 # CLI commands
├── auth/                # Authentication module
├── graph/               # Graph API clients
├── export/              # Export functionality
├── config/              # Configuration management
└── utils/               # Utility functions
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/overview)
- [MSAL Python](https://github.com/AzureAD/microsoft-authentication-library-for-python) 