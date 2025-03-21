#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Base Exporter
Base class for all exporters
"""

import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Union, Optional

from graphreporter.config.settings import get_settings


class BaseExporter(ABC):
    """
    Base class for all exporters
    
    Defines the interface that all exporters must implement
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the exporter
        
        Args:
            output_dir: Directory to save exported files
        """
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        
        # Use provided output directory or default from settings
        self.output_dir = output_dir or self.settings.output_dir
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.debug(f"Exporter initialized with output directory: {self.output_dir}")
    
    @abstractmethod
    def export(self, data: Union[List[Dict[str, Any]], Dict[str, Any]], filename: str) -> Path:
        """
        Export data to a file
        
        Args:
            data: Data to export
            filename: Name of the output file (without extension)
            
        Returns:
            Path: Path to the exported file
        """
        pass
    
    def _generate_filename(self, base_filename: str, extension: str) -> Path:
        """
        Generate a full file path with timestamp
        
        Args:
            base_filename: Base filename
            extension: File extension (without leading dot)
            
        Returns:
            Path: Full file path
        """
        # Add timestamp to filename to avoid overwriting
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{base_filename}_{timestamp}.{extension}"
        
        return self.output_dir / filename
    
    def _normalize_data(self, data: Union[List[Dict[str, Any]], Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize data to a list of dictionaries
        
        Args:
            data: Data to normalize
            
        Returns:
            List[Dict[str, Any]]: Normalized data
        """
        if isinstance(data, dict):
            # If data is a single dictionary, wrap it in a list
            if "value" in data and isinstance(data["value"], list):
                # If data is a Graph API response with a value array
                return data["value"]
            else:
                # If data is a single object
                return [data]
        elif isinstance(data, list):
            # If data is already a list
            return data
        else:
            # If data is something else, return an empty list
            self.logger.warning(f"Unsupported data type for export: {type(data)}")
            return [] 