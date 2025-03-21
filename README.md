# Project Template

A standardized project structure template with built-in memory system for documentation and development.

## Directory Structure

```
├── .cursor/rules/           # Cursor AI rules for project maintenance
├── .clinerules/             # CLI rules for project maintenance  
├── config/                  # Configuration files
├── data/                    # Data storage
├── docs/                    # Documentation
│   ├── architecture.md      # System architecture
│   ├── literature/          # Research and references
│   ├── product_requirement_docs.md  # Product requirements
│   └── technical.md         # Technical specifications
├── src/                     # Source code
├── tasks/                   # Task management
│   ├── active_context.md    # Current development focus
│   ├── rfc/                 # Request for comments
│   └── tasks_plan.md        # Task backlog and progress
├── test/                    # Test files
└── utils/                   # Utility scripts
```

## Getting Started

1. Click "Use this template" to create a new repository
2. Clone your new repository
3. Start developing with a pre-configured structure

## Memory System

This template implements a memory system using markdown files to track:

- Product requirements
- System architecture
- Technical specifications
- Active development context
- Task planning
- Error documentation
- Lessons learned

## Environment

- Configured for Windows Subsystem for Linux (WSL) or Linux server environments
- Bash shell commands recommended
- Includes rules for handling sudo privileged operations 