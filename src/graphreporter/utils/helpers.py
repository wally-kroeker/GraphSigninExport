"""
GraphReporter Utility Functions
Helper functions for the GraphReporter application
"""

import logging
from pathlib import Path
from typing import Optional


def setup_logging(log_level: str = "INFO", log_file: Optional[Path] = None) -> None:
    """
    Set up logging for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file for file logging
    """
    # Convert log level string to logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Basic configuration
    logging_config = {
        "level": numeric_level,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
    
    # Add file handler if log_file is provided
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logging_config["filename"] = str(log_file)
    
    # Apply configuration
    logging.basicConfig(**logging_config)
    
    # Set up logging for external libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("pandas").setLevel(logging.WARNING)
    
    # Log configuration
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {log_level}")


def format_file_size(size_bytes: int) -> str:
    """
    Format file size from bytes to human readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        str: Formatted file size (e.g., "1.23 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0 or unit == "TB":
            break
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} {unit}" 