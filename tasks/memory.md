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
- Future enhancement: Implement pagination to handle larger datasets

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