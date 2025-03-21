"""
GraphReporter Export Module
Provides export functionality for different formats
"""

from pathlib import Path
from typing import Optional

from graphreporter.export.base import BaseExporter
from graphreporter.export.csv_exporter import CSVExporter
from graphreporter.export.excel_exporter import ExcelExporter
from graphreporter.export.json_exporter import JSONExporter


def get_exporter(format_type: str, output_dir: Optional[Path] = None) -> BaseExporter:
    """
    Get an exporter instance based on the format type
    
    Args:
        format_type: Format type (csv, excel, json)
        output_dir: Directory to save exported files
        
    Returns:
        BaseExporter: Exporter instance
        
    Raises:
        ValueError: If format type is not supported
    """
    format_type = format_type.lower()
    
    if format_type == "csv":
        return CSVExporter(output_dir)
    elif format_type == "excel":
        return ExcelExporter(output_dir)
    elif format_type == "json":
        return JSONExporter(output_dir)
    else:
        raise ValueError(f"Unsupported format type: {format_type}")
