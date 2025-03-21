#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Graph Client
Base client for interacting with Microsoft Graph API
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union, Iterator

import requests
from requests.exceptions import RequestException

from graphreporter.auth.client import AuthClient
from graphreporter.config.settings import get_settings


class GraphClient:
    """
    Base client for Microsoft Graph API
    
    Handles common operations like requests, pagination, and error handling
    """
    
    def __init__(self):
        """Initialize the Graph client"""
        self.settings = get_settings()
        self.auth_client = AuthClient()
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        
        self.logger.debug("GraphClient initialized")
    
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to Microsoft Graph API
        
        Args:
            path: API path relative to graph endpoint
            params: Query parameters
            
        Returns:
            Dict[str, Any]: API response as a dictionary
            
        Raises:
            ValueError: If API request fails
        """
        url = f"{self.settings.graph_endpoint}/{path.lstrip('/')}"
        headers = self.auth_client.get_auth_header()
        
        self.logger.debug(f"Making GET request to {url}")
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            self.logger.error(f"Request to {url} failed: {str(e)}")
            
            # Handle rate limiting
            if response.status_code == 429:
                self._handle_rate_limiting(response)
                # Retry the request recursively (with care for stack depth)
                return self.get(path, params)
            
            # Handle authentication errors
            if response.status_code == 401:
                self.logger.error("Authentication failed, token might be expired or invalid")
            
            # Try to get response content for better error messages
            error_details = "Unknown error"
            try:
                error_details = response.json()
            except ValueError:
                error_details = response.text
            
            raise ValueError(f"Graph API request failed: {error_details}")
    
    def get_paginated(self, path: str, params: Optional[Dict[str, Any]] = None) -> Iterator[Dict[str, Any]]:
        """
        Get paginated results from Microsoft Graph API
        
        Yields individual items from the 'value' array in the response,
        automatically handling pagination via @odata.nextLink
        
        Args:
            path: API path relative to graph endpoint
            params: Query parameters
            
        Yields:
            Dict[str, Any]: Individual items from the response
        """
        if params is None:
            params = {}
        
        next_link = None
        first_request = True
        
        while first_request or next_link:
            if first_request:
                # First request uses the provided path and params
                response = self.get(path, params)
                first_request = False
            else:
                # Subsequent requests use the nextLink directly
                self.logger.debug(f"Following next link: {next_link}")
                response = self.session.get(next_link, headers=self.auth_client.get_auth_header()).json()
            
            # Extract items from the response
            items = response.get("value", [])
            for item in items:
                yield item
            
            # Get the next link for pagination
            next_link = response.get("@odata.nextLink")
    
    def _handle_rate_limiting(self, response: requests.Response) -> None:
        """
        Handle rate limiting by Microsoft Graph API
        
        Args:
            response: Response with rate limiting headers
        """
        retry_after = int(response.headers.get("Retry-After", 1))
        self.logger.warning(f"Rate limited by Microsoft Graph API. Waiting {retry_after} seconds.")
        time.sleep(retry_after) 