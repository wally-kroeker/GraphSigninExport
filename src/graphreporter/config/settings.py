#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Configuration
Manages application settings and configuration
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings class
    
    Loads configuration from environment variables
    """
    # Required settings
    tenant_id: str = Field(..., env="GRAPH_TENANT_ID")
    client_id: str = Field(..., env="GRAPH_CLIENT_ID")
    client_secret: str = Field(..., env="GRAPH_CLIENT_SECRET")
    
    # Optional settings with defaults
    authority_url: Optional[str] = Field(None, env="GRAPH_AUTHORITY_URL")
    scopes: List[str] = Field(["https://graph.microsoft.com/.default"], env="GRAPH_SCOPES")
    graph_endpoint: str = Field("https://graph.microsoft.com/v1.0", env="GRAPH_ENDPOINT")
    
    # Output settings
    output_format: str = Field("csv", env="GRAPH_OUTPUT_FORMAT")
    output_dir: Path = Field(Path("./output"), env="GRAPH_OUTPUT_DIR")
    
    # Logging settings
    log_level: str = Field("INFO", env="GRAPH_LOG_LEVEL")
    
    @validator("authority_url", pre=True, always=True)
    def set_authority_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Set authority URL based on tenant ID if not provided"""
        if v:
            return v
        
        tenant_id = values.get("tenant_id")
        if tenant_id:
            return f"https://login.microsoftonline.com/{tenant_id}"
        
        # This should never happen due to the required field constraint
        raise ValueError("tenant_id is required to construct authority_url")
    
    @validator("output_dir", pre=True)
    def create_output_dir(cls, v: Union[str, Path]) -> Path:
        """Create output directory if it doesn't exist"""
        output_dir = Path(v)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Function to get settings instance
def get_settings() -> Settings:
    """
    Get application settings
    
    Returns:
        Settings: Application settings
    """
    return Settings() 