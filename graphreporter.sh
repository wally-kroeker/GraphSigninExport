#!/bin/bash

# GraphReporter CLI
# A command-line interface for exporting Microsoft Graph sign-in logs
# Version: 1.0.0

# Set the base directory to the location of this script
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$BASE_DIR/.venv"
EXPORT_DIR="$BASE_DIR/exports"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Display help information
show_help() {
    cat << EOF
GraphReporter CLI
A command-line interface for exporting Microsoft Graph sign-in logs

Usage: ./graphreporter.sh <command> [options]

Commands:
  setup                  Set up the Python environment and install dependencies
  signin                 Export all sign-in logs
  app-by-name <app_name> Export sign-in logs for an app by display name
  app-by-id <app_id>     Export sign-in logs for an app by ID
  user <email>           Export sign-in logs for a specific user
  help                   Show this help message

Common Options:
  --days <number>        Number of days to look back (default: 7)
  --chunk-days <number>  Number of days per chunk to avoid timeouts (default: 5)
  --no-combine          Do not combine multiple CSV files into one
  --verbose             Enable verbose output

Examples:
  ./graphreporter.sh setup
  ./graphreporter.sh signin --days 30
  ./graphreporter.sh app-by-name "Office365 Shell WCSS-Client" --days 14
  ./graphreporter.sh app-by-id 6a08801d-62d2-4770-91d1-cc1887a0e884 --days 90 --chunk-days 10
  ./graphreporter.sh user user@example.com --days 7

Environment Setup:
  1. Clone the repository
  2. Create a .env file in the project root with:
     - AZURE_TENANT_ID
     - AZURE_CLIENT_ID
     - AZURE_CLIENT_SECRET
  3. Run './graphreporter.sh setup' to create the UV environment

For more information, visit: https://github.com/wally-kroeker/GraphSigninExport
EOF
}

# Check if UV is installed
check_uv() {
    if ! command -v uv &> /dev/null; then
        log_error "UV (Astral) is not installed. Please install it first:"
        log_error "curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
}

# Set up Python environment using UV
setup_environment() {
    log_info "Setting up Python environment using UV..."
    
    # Check if UV is installed
    check_uv
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Creating virtual environment..."
        execute_command uv venv "$VENV_DIR"
    fi
    
    # Install dependencies using UV
    log_info "Installing dependencies..."
    execute_command uv pip install -r "$BASE_DIR/requirements.txt"
    
    log_info "Environment setup completed successfully!"
}

# Check environment setup
check_environment() {
    # Check if UV is installed
    check_uv
    
    # Check if .env file exists
    if [ ! -f "$BASE_DIR/.env" ]; then
        log_error "Missing .env file. Please create one with required Azure credentials."
        exit 1
    fi

    # Check if virtual environment exists
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        log_error "Virtual environment not found. Please run: ./graphreporter.sh setup"
        exit 1
    fi

    # Create exports directory if it doesn't exist
    if [ ! -d "$EXPORT_DIR" ]; then
        log_info "Creating exports directory..."
        mkdir -p "$EXPORT_DIR"
    fi
}

# Activate virtual environment
activate_venv() {
    log_info "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
}

# Execute a command with proper error handling
execute_command() {
    if [ "$VERBOSE" = true ]; then
        log_info "Running: $@"
    fi
    
    "$@"
    exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        log_error "Command failed with exit code $exit_code"
        exit $exit_code
    fi
}

# Initialize variables
VERBOSE=false

# Check if a command is provided
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

# Parse the command
command="$1"
shift

case "$command" in
    setup)
        setup_environment
        exit 0
        ;;
        
    signin|app-by-name|app-by-id|user)
        # Check environment and activate virtual environment
        check_environment
        activate_venv
        
        case "$command" in
            signin)
                days=7
                
                # Parse options
                while [[ $# -gt 0 ]]; do
                    case "$1" in
                        --days)
                            days="$2"
                            shift 2
                            ;;
                        --verbose)
                            VERBOSE=true
                            shift
                            ;;
                        *)
                            log_error "Unknown option: $1"
                            show_help
                            exit 1
                            ;;
                    esac
                done
                
                log_info "Exporting sign-in logs for the last $days days..."
                execute_command python "$BASE_DIR/examples/export_signin_logs.py" --days "$days"
                ;;
                
            app-by-name)
                if [ $# -lt 1 ]; then
                    log_error "Missing application name"
                    show_help
                    exit 1
                fi
                
                app_name="$1"
                shift
                days=7
                chunk_days=5
                combine=""
                
                # Parse options
                while [[ $# -gt 0 ]]; do
                    case "$1" in
                        --days)
                            days="$2"
                            shift 2
                            ;;
                        --chunk-days)
                            chunk_days="$2"
                            shift 2
                            ;;
                        --no-combine)
                            combine="--no-combine"
                            shift
                            ;;
                        --verbose)
                            VERBOSE=true
                            shift
                            ;;
                        *)
                            log_error "Unknown option: $1"
                            show_help
                            exit 1
                            ;;
                    esac
                done
                
                log_info "Exporting sign-in logs for application '$app_name' for the last $days days..."
                log_info "Using chunk size of $chunk_days days..."
                execute_command python "$BASE_DIR/examples/export_enterprise_app_logs.py" "$app_name" --days "$days" --chunk-days "$chunk_days" $combine
                ;;
                
            app-by-id)
                if [ $# -lt 1 ]; then
                    log_error "Missing application ID"
                    show_help
                    exit 1
                fi
                
                app_id="$1"
                shift
                days=90
                chunk_days=10
                combine="--combine"
                
                # Parse options
                while [[ $# -gt 0 ]]; do
                    case "$1" in
                        --days)
                            days="$2"
                            shift 2
                            ;;
                        --chunk-days)
                            chunk_days="$2"
                            shift 2
                            ;;
                        --no-combine)
                            combine="--no-combine"
                            shift
                            ;;
                        --verbose)
                            VERBOSE=true
                            shift
                            ;;
                        *)
                            log_error "Unknown option: $1"
                            show_help
                            exit 1
                            ;;
                    esac
                done
                
                log_info "Exporting sign-in logs for application ID '$app_id' for the last $days days..."
                log_info "Using chunk size of $chunk_days days..."
                execute_command python "$BASE_DIR/examples/export_app_by_id.py" "$app_id" --days "$days" --chunk-days "$chunk_days" $combine
                ;;
                
            user)
                if [ $# -lt 1 ]; then
                    log_error "Missing user email"
                    show_help
                    exit 1
                fi
                
                user_email="$1"
                shift
                days=7
                
                # Parse options
                while [[ $# -gt 0 ]]; do
                    case "$1" in
                        --days)
                            days="$2"
                            shift 2
                            ;;
                        --chunk-days)
                            chunk_days="$2"
                            shift 2
                            ;;
                        --no-combine)
                            no_combine="--no-combine"
                            shift
                            ;;
                        --verbose)
                            VERBOSE=true
                            shift
                            ;;
                        *)
                            log_error "Unknown option: $1"
                            show_help
                            exit 1
                            ;;
                    esac
                done
                
                log_info "Exporting sign-in logs for user '$user_email' for the last $days days..."
                # Set defaults for optional parameters
                chunk_days=${chunk_days:-3}
                no_combine=${no_combine:-""}
                
                execute_command python "$BASE_DIR/examples/export_user_signin_logs.py" "$user_email" --days "$days" --chunk-days "$chunk_days" $no_combine
                ;;
        esac
        ;;
        
    help)
        show_help
        ;;
        
    *)
        log_error "Unknown command: $command"
        show_help
        exit 1
        ;;
esac

log_info "Export completed successfully!"
exit 0 