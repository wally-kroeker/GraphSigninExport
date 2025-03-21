#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter JSON Exporter
Exports data to JSON format
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Union, Optional

from graphreporter.export.base import BaseExporter


class JSONExporter(BaseExporter):
    """
    Exporter for JSON format
    
    Exports data to JSON files
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the JSON exporter
        
        Args:
            output_dir: Directory to save exported files
        """
        super().__init__(output_dir)
        self.logger = logging.getLogger(__name__)
        
        self.logger.debug("JSONExporter initialized")
    
    def export(self, data: Union[List[Dict[str, Any]], Dict[str, Any]], filename: str) -> Path:
        """
        Export data to a JSON file
        
        Args:
            data: Data to export
            filename: Name of the output file (without extension)
            
        Returns:
            Path: Path to the exported file
        """
        self.logger.info(f"Exporting data to JSON: {filename}")
        
        # Normalize data to a list of dictionaries
        normalized_data = self._normalize_data(data)
        
        if not normalized_data:
            self.logger.warning("No data to export")
            raise ValueError("No data to export")
        
        # Generate output file path
        output_file = self._generate_filename(filename, "json")
        
        # Export to JSON
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(normalized_data, file, indent=2, default=self._json_serializer)
        
        self.logger.info(f"Data exported to {output_file}")
        return output_file
    
    def _json_serializer(self, obj: Any) -> Any:
        """
        Custom JSON serializer for handling objects that are not JSON serializable
        
        Args:
            obj: Object to serialize
            
        Returns:
            Any: Serialized object
        """
        # Handle datetime objects
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        
        # Handle other non-serializable objects
        return str(obj) 