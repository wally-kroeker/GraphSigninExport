# Product Requirements

## Project Overview

GraphReporter is a Python-based CLI tool that uses Microsoft Graph API to retrieve and report data from Microsoft Entra ID (Azure AD). The tool is designed for IT administrators and security professionals who need to analyze sign-in logs, app registrations, and enterprise apps.

## Problem Statement

Organizations using Microsoft 365 and Azure need a way to efficiently extract and analyze data from their Microsoft Entra ID (Azure AD) environment. This data is essential for security auditing, compliance reporting, and operational insights. While this data is available through the Microsoft Graph API, there's a need for a simple, command-line tool that can extract this data in formats suitable for analysis.

## Goals and Objectives

1. Create a Python-based CLI tool that interfaces with Microsoft Graph API
2. Retrieve sign-in logs, app registrations, and enterprise apps data
3. Export data in multiple formats (CSV, Excel, JSON) for further analysis
4. Ensure secure authentication using client credentials flow
5. Implement robust error handling and logging
6. Support filtering and pagination for large datasets

## User Stories

### As an IT Administrator:
- I want to retrieve sign-in logs for the last 7 days to review authentication patterns
- I want to export all app registrations to CSV to audit application permissions
- I want to list all enterprise apps to review external service integrations
- I want to filter sign-in logs by date range and export to Excel for compliance reporting

### As a Security Analyst:
- I want to identify all sign-ins from suspicious locations or with unusual patterns
- I want to audit app registrations with high privilege permissions
- I want to review recently added enterprise applications for security assessment

## Requirements

### Functional Requirements

1. **Authentication**
   - Authenticate using client credentials (app-only) flow
   - Use MSAL Python library for authentication
   - Support secure storage and management of credentials
   - Implement immediate revocation if credentials are changed in Azure

2. **Data Retrieval**
   - Retrieve sign-in logs with filtering capabilities
   - List all app registrations with detailed permissions
   - List all enterprise apps (service principals) with access information
   - Handle pagination for large datasets
   - Support filtering by date ranges and other relevant properties

3. **Output Formats**
   - Export data to CSV files
   - Export data to Excel files with basic formatting
   - Support JSON output for programmatic consumption
   - Include headers and metadata in exports

4. **Command Line Interface**
   - Provide intuitive commands for different data types
   - Support command-line arguments for filtering and output options
   - Include help documentation for all commands
   - Display progress for long-running operations

### Non-Functional Requirements

1. **Performance**
   - Efficiently handle large datasets with pagination
   - Minimize API calls to prevent throttling
   - Optimize memory usage when processing large result sets

2. **Security**
   - Securely store and handle credentials
   - Never log or expose sensitive information
   - Implement proper error handling that doesn't expose security details
   - Support credential revocation mechanisms

3. **Usability**
   - Clear and consistent command syntax
   - Helpful error messages and logging
   - Progress indicators for long-running operations
   - Comprehensive documentation and examples

4. **Maintainability**
   - Modular code architecture
   - Comprehensive test coverage
   - Clear code documentation
   - Version control and release management

## Success Criteria

1. The tool successfully authenticates with Microsoft Graph API using client credentials
2. All required data types can be retrieved and exported in specified formats
3. The CLI interface is intuitive and well-documented
4. The tool handles errors gracefully with helpful messages
5. Performance is acceptable with large datasets
6. Security requirements are fully implemented

## Constraints

1. The tool must use the Microsoft Graph API V1.0 endpoints
2. Authentication must use client credentials flow with a client secret
3. The application requires the following API permissions:
   - AuditLog.Read.All (application permission)
   - Directory.Read.All (application permission)
   - Application.Read.All (application permission)
4. The tool must be developed in Python 3.8+
