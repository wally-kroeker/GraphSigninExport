# Tasks Plan

This document outlines the planned tasks and their current status for the GraphReporter project.

## Environment Setup

- [x] Initialize project structure
- [x] Create virtual environment with UV (Astral)
- [x] Set up Git repository
- [x] Configure development tools (black, isort, flake8)
- [x] Create pyproject.toml for modern Python packaging
- [x] Generate requirements files using UV
- [x] Set up pytest for testing
- [x] Set up configuration management

## Authentication Module

- [x] Create AuthClient using azure-identity
- [x] Implement client credentials flow
- [x] Add basic authentication test
- [ ] Add token caching and management
- [ ] Handle authentication errors gracefully
- [ ] Write additional unit tests for auth module

## Microsoft Graph API Integration

- [x] Implement SignInLogsClient for retrieving sign-in logs
- [x] Add filtering capabilities (date range, application, user)
- [x] Create CSV export functionality
- [x] Create example scripts for different export scenarios
- [x] Enhance export scripts with chunking to handle timeouts
- [x] Add automatic file combining for chunked exports
- [ ] Implement pagination handling for large datasets
- [ ] Add retry logic for failed API calls
- [ ] Add more comprehensive logging

## CLI Interface Implementation

- [x] Create graphreporter.sh shell script:
  - [x] Implement command structure (signin, app-by-name, app-by-id, user)
  - [x] Add common options (--days, --chunk-days, --no-combine)
  - [x] Add environment setup and validation
  - [x] Add UV environment management and setup command
  - [x] Implement help system with examples
  - [x] Add error handling and logging
- [x] Update example scripts for CLI compatibility:
  - [x] Add consistent command-line arguments to all scripts
  - [x] Update export_signin_logs.py with --days parameter
  - [x] Update export_enterprise_app_logs.py with app name argument
  - [x] Update export_user_signin_logs.py with email argument
  - [x] Standardize output formatting across all scripts
- [x] Add CLI documentation:
  - [x] Update README with CLI usage instructions
  - [x] Add examples for each command type
  - [x] Document common options and parameters
  - [x] Add troubleshooting guide
  - [x] Document UV setup and requirements
- [ ] Extend CLI interface:
  - [ ] Add more report types as they are developed
  - [ ] Add output format selection options
  - [ ] Add advanced filtering parameters
  - [ ] Implement configuration customization

## Data Export and Reporting

- [x] Implement basic CSV export
- [x] Create command-line interface for specific report types
- [ ] Add Excel export format
- [ ] Add JSON export format
- [ ] Create report templates
- [ ] Implement data visualization options
- [ ] Add scheduling capability for recurring reports

## Additional Report Types

- [ ] Device information reports
- [ ] User information reports
- [ ] Application usage reports
- [ ] License usage reports
- [ ] Security alerts reports

## Project Documentation

- [x] Create product requirements document
- [x] Document architecture
- [x] Document technical setup
- [x] Create tasks plan
- [x] Maintain active context
- [x] Document Microsoft Graph API best practices
- [ ] Write developer guide
- [ ] Write user guide

## Testing and Quality Assurance

- [x] Implement basic unit tests
- [ ] Add integration tests
- [ ] Set up CI/CD pipeline
- [ ] Implement code coverage reporting
- [ ] Add load testing for large dataset handling

## Deployment and Distribution

- [ ] Package the application
- [ ] Create installation documentation
- [ ] Set up automated releases
- [ ] Create Docker image
