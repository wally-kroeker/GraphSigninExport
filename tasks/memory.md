# Project Memory

This document keeps track of the project's history, key decisions, and milestones. It serves as long-term memory for the project.

## Project Timeline

### March 21, 2025

- Successfully implemented the Sign-In Logs export functionality
- Created example scripts for:
  - General sign-in logs export
  - Enterprise application-specific sign-in logs export
  - User-specific sign-in logs export
- Updated authentication module to use the latest Microsoft Graph SDK
- Migrated the repository to https://github.com/wally-kroeker/GraphSigninExport
- Updated project documentation and lessons learned
- Learned and implemented Microsoft's best practices for avoiding timeouts and throttling

### March 22, 2025

- Enhanced the application-specific sign-in logs export script:
  - Fixed issues with date range handling to prevent infinite loops
  - Improved error handling for API timeouts
  - Implemented chunking of large date ranges to improve reliability
  - Added automatic file combining functionality to merge chunked exports
  - Added command-line arguments for flexible date ranges and chunk sizes
- Enhanced user-specific sign-in logs export script:
  - Implemented time chunking strategy to address timeout issues
  - Added proper error handling for each chunk
  - Added automatic CSV file combining functionality
  - Added support for command-line arguments (chunk-days, no-combine)
- Created unified shell script interface (graphreporter.sh) for the entire project:
  - Added commands for each export type (signin, app-by-name, app-by-id, user)
  - Implemented UV-based environment setup and validation
  - Added comprehensive help system with examples
  - Added error handling and logging
  - Standardized command-line arguments across all scripts
- Updated project documentation to reflect all recent improvements

### March 23, 2025

- Fixed critical issue with hardcoded application name in enterprise app logs export script
- Enhanced example scripts to avoid hardcoded values:
  - Removed hardcoded application name "Office365 Shell WCSS-Client"
  - Previously fixed hardcoded user email
  - All parameters now properly passed via command-line arguments
- Improved script flexibility and reusability through proper parameterization

### March 24, 2025

- Enhanced enterprise app logs export script with time chunking:
  - Added support for breaking large date ranges into smaller chunks
  - Implemented automatic file combining functionality
  - Added command-line arguments for chunk size control
  - Fixed timeout issues when requesting large date ranges
  - Aligned with the same chunking strategy used in app-by-id and user scripts
- Standardized chunking implementation across all export scripts:
  - Default chunk size of 5 days for enterprise apps
  - Automatic file combining with option to preserve individual chunks
  - Consistent error handling and progress reporting

## Key Decisions

### Authentication Approach

- Using app-only (client credentials) authentication with Azure AD
- Required permissions: AuditLog.Read.All, Directory.Read.All
- Important: The Azure AD application must be properly registered and granted admin consent

### Data Export Strategy

- CSV as the primary export format for sign-in logs
- Focused on three main query types:
  1. All sign-in logs within a date range
  2. Enterprise application-specific sign-in logs
  3. User-specific sign-in logs
- Currently retrieving up to 1000 records per query
- Breaking large date ranges into smaller chunks (5-10 days) to avoid timeouts
- Using proper error handling to ensure partial success in case of failures
- Automatically combining chunked exports into a single file for ease of analysis
- Future enhancement: Implement pagination to handle larger datasets

### Microsoft Graph API Best Practices

- Breaking requests into smaller time chunks to avoid timeouts (implemented across all scripts):
  - User sign-in logs: 3-day chunks
  - Enterprise app logs: 5-day chunks
  - App-by-id logs: 10-day chunks
- Using asynchronous requests with proper error handling (implemented)
- Properly setting up authentication with correct scopes (implemented)
- Implemented safety checks to prevent infinite loops when processing date ranges
- Implemented file combining to enhance usability of chunked exports
- Future improvements:
  - Implement batching for multiple simultaneous requests
  - Use select parameter to request only needed fields
  - Implement retry logic with exponential backoff
  - Consider Microsoft Graph Data Connect for bulk data extraction

### CLI Interface Design

- Created a unified shell script interface (graphreporter.sh):
  - Simple and intuitive command structure
  - Consistent parameter naming across all scripts
  - All parameters passed via command-line arguments (no hardcoded values)
  - Automatic environment setup and validation
  - Built-in help and examples
- Used UV (Astral) for environment management:
  - Automatic virtual environment creation
  - Package installation via UV
  - Environment validation checks
- Standardized reporting across all exports:
  - Consistent file naming conventions
  - Similar output formatting
  - Automatic CSV file combining when chunking is used

### Code Quality and Maintainability

- Strict avoidance of hardcoded values in example scripts:
  - All parameters passed via command-line arguments
  - Default values set through argparse when appropriate
  - Clear documentation of required and optional parameters
- Consistent error handling and logging across all scripts
- Modular design with reusable components
- Clear separation of concerns between authentication, data retrieval, and export functionality

### Project Structure

- Modular design with separate client classes for different Graph API areas
- Base authentication client that other clients can build upon
- Separate example scripts for different use cases
- Exports directory for storing output files
- Comprehensive documentation in the tasks directory
- Unified shell script interface for all functionality

## Next Steps

- Add pagination support for handling datasets larger than 1000 records
- Implement additional filtering options (IP address, location, etc.)
- Add support for exporting in different formats (JSON, Excel)
- Enhance error handling and logging
- Create additional example scripts for other use cases
- Implement batch requests for more efficient API calls
- Add retry logic with exponential backoff for failed requests 