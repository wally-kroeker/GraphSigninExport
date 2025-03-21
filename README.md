# GraphReporter

A Python CLI tool for retrieving and reporting Microsoft Entra ID (Azure AD) sign-in logs using Microsoft Graph API.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

GraphReporter is a command-line tool that helps IT administrators and security professionals extract and analyze sign-in logs from Microsoft Entra ID (Azure AD). It uses the Microsoft Graph API to retrieve sign-in logs with flexible filtering options by application, user, or date range.

### Features

- **Authentication**: Secure client credentials (app-only) authentication with Microsoft Graph API
- **Sign-in Logs**: Fetch sign-in logs with various filtering options
  - All sign-ins within a date range
  - Application-specific sign-ins (by name or ID)
  - User-specific sign-ins
- **Smart Data Retrieval**: 
  - Automatic chunking of large date ranges to avoid timeouts
  - File combining for chunked exports
  - Configurable chunk sizes
- **Export**: Export data to CSV format (Excel and JSON coming soon)
- **Easy to Use**: Simple shell script interface for all operations

## Prerequisites

Before using GraphReporter, you need to:

1. Register an application in Microsoft Entra ID (Azure AD)
2. Grant the following API permissions:
   - AuditLog.Read.All (Application)
   - Directory.Read.All (Application)
3. Generate a client secret

## Quick Start

```bash
# 1. Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone the repository
git clone https://github.com/wally-kroeker/GraphSigninExport.git
cd GraphSigninExport

# 3. Create .env file with your Azure credentials
cat > .env << EOF
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
EOF

# 4. Set up the environment
./graphreporter.sh setup

# 5. Start using the tool!
./graphreporter.sh signin --days 7
```

## Usage

GraphReporter provides several commands to export sign-in logs:

### Export All Sign-in Logs
```bash
# Export last 7 days of sign-ins (default)
./graphreporter.sh signin

# Export sign-ins for a specific number of days
./graphreporter.sh signin --days 30
```

### Export Application-Specific Logs
```bash
# By application display name
./graphreporter.sh app-by-name "Office365 Shell WCSS-Client" --days 14

# By application ID with chunking
./graphreporter.sh app-by-id 6a08801d-62d2-4770-91d1-cc1887a0e884 --days 90 --chunk-days 10
```

### Export User-Specific Logs
```bash
# Export sign-ins for a specific user
./graphreporter.sh user user@example.com --days 7
```

### Common Options
```bash
  --days <number>        Number of days to look back (default: 7)
  --chunk-days <number>  Number of days per chunk to avoid timeouts (default: 5)
  --no-combine          Do not combine multiple CSV files into one
  --verbose             Enable verbose output
```

### Get Help
```bash
# Show all available commands and options
./graphreporter.sh help
```

## Output

All exports are saved in the `exports/` directory in CSV format. The files are named based on the type of export and date range:

- All sign-ins: `signin_logs_YYYY-MM-DD_YYYY-MM-DD.csv`
- App-specific: `app_logs_AppName_YYYY-MM-DD_YYYY-MM-DD.csv`
- User-specific: `user_logs_username_YYYY-MM-DD_YYYY-MM-DD.csv`

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/wally-kroeker/GraphSigninExport.git
cd GraphSigninExport

# Install UV (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up the environment
./graphreporter.sh setup

# Install development dependencies
uv pip install -r requirements-dev.txt
```

### Project Structure

```
GraphSigninExport/
├── src/
│   └── graphreporter/
│       ├── auth/           # Authentication module
│       │   └── client.py   # AuthClient for Graph API
│       ├── config/         # Configuration settings
│       └── reports/        # Report generation modules
├── examples/               # Example scripts
├── tests/                 # Test files
├── exports/               # Output directory
├── graphreporter.sh       # CLI interface
└── requirements.txt       # Project dependencies
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=graphreporter
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your Azure AD credentials in the `.env` file
   - Ensure proper API permissions are granted
   - Check if admin consent is provided for the permissions

2. **Timeout Errors**
   - Use the `--chunk-days` option to reduce the time range per request
   - For large exports, use the `app-by-id` command which supports chunking

3. **Environment Issues**
   - Run `./graphreporter.sh setup` to reset the environment
   - Ensure UV is installed and in your PATH
   - Check if the virtual environment is activated

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/overview)
- [Azure Identity Python SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity) 