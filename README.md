# Project Template

A standardized project structure template with built-in memory system for documentation and development. This template enforces strict development practices through a comprehensive ruleset and structured documentation approach.

## Directory Structure

```
├── .cursor/rules/           # Cursor AI rules for project maintenance
│   ├── rules.mdc           # Core development rules and workflows
│   ├── memory.mdc          # Memory system specifications
│   ├── error-documentation.mdc  # Error tracking and solutions
│   └── lessons-learned.mdc  # Project learnings and patterns
├── .clinerules/            # CLI rules for project maintenance  
│   ├── rules.md           # CLI-specific development rules
│   ├── memory.md          # Memory system implementation
│   └── directory-structure.md  # Directory organization rules
├── config/                 # Configuration files
├── data/                   # Data storage
├── docs/                   # Documentation
│   ├── architecture.md     # System architecture
│   ├── literature/         # Research and references
│   ├── product_requirement_docs.md  # Product requirements
│   └── technical.md        # Technical specifications
├── src/                    # Source code
├── tasks/                  # Task management
│   ├── active_context.md   # Current development focus
│   ├── rfc/               # Request for comments
│   └── tasks_plan.md      # Task backlog and progress
├── test/                   # Test files
└── utils/                  # Utility scripts
```

## Getting Started

1. Click "Use this template" to create a new repository
2. Clone your new repository
3. Set up your development environment:
   - Ensure you're using WSL or a Linux environment
   - Install required tools (bash, git)
   - Install UV (Astral) for Python environment management
4. Initialize your project:
   - Review and customize the documentation templates in `docs/`
   - Set up your project's Python environment using UV
   - Start developing with the pre-configured structure

## Memory System

This template implements a comprehensive memory system using markdown files to track project evolution and maintain consistent development practices:

### Core Documentation
- `product_requirement_docs.md`: Product requirements and scope
- `architecture.md`: System architecture and component relationships
- `technical.md`: Technical specifications and stack details
- `tasks_plan.md`: Task backlog and project progress

### Active Development
- `active_context.md`: Current development focus and state
- `error-documentation.mdc`: Known issues and their resolutions
- `lessons-learned.mdc`: Project patterns and intelligence

### Documentation Flow
1. Requirements flow from product docs to architecture
2. Architecture informs technical decisions
3. Technical specs guide task planning
4. Active context tracks current progress
5. Errors and lessons are continuously documented

## Development Rules

### Environment Specifications
- **Platform**: Windows Subsystem for Linux (WSL) or Linux server
- **Shell**: All commands MUST use bash shell (PowerShell prohibited)
- **Sudo Operations**: Strict protocol for privileged operations
- **Python Environment**:
  - UV (Astral) required for all Python operations
  - Virtual environments managed via `uv venv`
  - Package management exclusively through `uv pip`
  - Dependencies tracked in `requirements.txt`

### Development Workflow
1. **Planning Mode**:
   - Requirement analysis and clarification
   - Solution design and validation
   - Architecture alignment check

2. **Implementation Mode**:
   - Systematic code changes
   - Incremental rollouts
   - Comprehensive testing
   - Documentation updates

3. **Quality Assurance**:
   - Automated testing
   - Code review guidelines
   - Documentation requirements
   - Error tracking and resolution

## Maintenance

The template includes automated processes for:
- Tracking development context
- Documenting errors and solutions
- Capturing project learnings
- Maintaining consistent practices

## Contributing

1. Follow the established directory structure
2. Adhere to the documentation requirements
3. Use the prescribed development workflow
4. Update memory system files as you work
5. Document any deviations or improvements

## License

[Your License Here] 