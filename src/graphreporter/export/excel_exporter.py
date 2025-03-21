#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Excel Exporter
Exports data to Excel format
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Union, Optional

import pandas as pd

from graphreporter.export.base import BaseExporter


class ExcelExporter(BaseExporter):
    """
    Exporter for Excel format
    
    Exports data to Excel files using pandas and openpyxl
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the Excel exporter
        
        Args:
            output_dir: Directory to save exported files
        """
        super().__init__(output_dir)
        self.logger = logging.getLogger(__name__)
        
        self.logger.debug("ExcelExporter initialized")
    
    def export(self, data: Union[List[Dict[str, Any]], Dict[str, Any]], filename: str) -> Path:
        """
        Export data to an Excel file
        
        Args:
            data: Data to export
            filename: Name of the output file (without extension)
            
        Returns:
            Path: Path to the exported file
        """
        self.logger.info(f"Exporting data to Excel: {filename}")
        
        # Normalize data to a list of dictionaries
        normalized_data = self._normalize_data(data)
        
        if not normalized_data:
            self.logger.warning("No data to export")
            raise ValueError("No data to export")
        
        # Convert to DataFrame
        df = pd.DataFrame(normalized_data)
        
        # Flatten nested objects if needed
        df = self._flatten_dataframe(df)
        
        # Generate output file path
        output_file = self._generate_filename(filename, "xlsx")
        
        # Export to Excel
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Data", index=False)
            self._format_worksheet(writer, df)
        
        self.logger.info(f"Data exported to {output_file}")
        return output_file
    
    def _flatten_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Flatten nested objects in DataFrame
        
        Args:
            df: DataFrame to flatten
            
        Returns:
            pd.DataFrame: Flattened DataFrame
        """
        # Get a list of columns that contain dictionaries or lists
        nested_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
                if isinstance(sample, (dict, list)):
                    nested_columns.append(col)
        
        # If no nested columns, return as is
        if not nested_columns:
            return df
        
        # Drop nested columns (we'll convert them to string representation)
        flat_df = df.drop(columns=nested_columns)
        
        # Convert nested columns to string representation
        for col in nested_columns:
            flat_df[col] = df[col].apply(lambda x: str(x) if x is not None else None)
        
        return flat_df
    
    def _format_worksheet(self, writer: pd.ExcelWriter, df: pd.DataFrame) -> None:
        """
        Format Excel worksheet
        
        Args:
            writer: Excel writer
            df: DataFrame being exported
        """
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets["Data"]
        
        # Format header row
        header_format = {
            "bold": True,
            "bg_color": "#4472C4",
            "font_color": "white",
            "border": 1
        }
        
        # Set column widths
        for i, column in enumerate(df.columns):
            # Estimate column width based on header and data
            max_len = max(
                len(str(column)),
                df[column].astype(str).map(len).max() if not df.empty else 0
            )
            max_len = min(max_len, 50)  # Cap at 50 characters
            worksheet.column_dimensions[chr(65 + i)].width = max_len + 2 