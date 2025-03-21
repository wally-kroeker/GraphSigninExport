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

- Breaking requests into smaller time chunks to avoid timeouts (implemented)
- Using asynchronous requests with proper error handling (implemented)
- Properly setting up authentication with correct scopes (implemented)
- Implemented safety checks to prevent infinite loops when processing date ranges
- Implemented file combining to enhance usability of chunked exports
- Future improvements:
  - Implement batching for multiple simultaneous requests
  - Use select parameter to request only needed fields
  - Implement retry logic with exponential backoff
  - Consider Microsoft Graph Data Connect for bulk data extraction

### Project Structure

- Modular design with separate client classes for different Graph API areas
- Base authentication client that other clients can build upon
- Separate example scripts for different use cases
- Exports directory for storing output files
- Comprehensive documentation in the tasks directory

## Next Steps

- Add pagination support for handling datasets larger than 1000 records
- Implement additional filtering options (IP address, location, etc.)
- Add support for exporting in different formats (JSON, Excel)
- Enhance error handling and logging
- Create additional example scripts for other use cases
- Implement batch requests for more efficient API calls
- Add retry logic with exponential backoff for failed requests 