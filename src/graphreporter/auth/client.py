#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Authentication Client
Handles authentication with Microsoft Graph API using MSAL
"""

import logging
from typing import Dict, List, Optional, Any

import msal

from graphreporter.config.settings import get_settings


class AuthClient:
    """
    Authentication client for Microsoft Graph API
    
    Uses MSAL to implement client credentials flow
    """
    
    def __init__(self):
        """Initialize the authentication client"""
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
        self._app = None
        self._token_cache = {}
        
        self.logger.debug("AuthClient initialized")
    
    @property
    def app(self) -> msal.ConfidentialClientApplication:
        """
        Get or create the MSAL confidential client application
        
        Returns:
            msal.ConfidentialClientApplication: MSAL client application
        """
        if not self._app:
            self.logger.debug("Creating MSAL confidential client application")
            self._app = msal.ConfidentialClientApplication(
                client_id=self.settings.client_id,
                client_credential=self.settings.client_secret,
                authority=self.settings.authority_url,
            )
        return self._app
    
    def get_token(self) -> Optional[str]:
        """
        Acquire a token for Microsoft Graph API
        
        Returns:
            Optional[str]: Access token or None if acquisition failed
        """
        self.logger.debug("Acquiring token for client")
        
        # Try to get token from cache first
        if self._token_cache:
            self.logger.debug("Checking token cache")
            if "access_token" in self._token_cache and not self._is_token_expired():
                self.logger.debug("Using cached token")
                return self._token_cache["access_token"]
        
        # Acquire new token
        self.logger.debug("Acquiring new token")
        result = self.app.acquire_token_for_client(scopes=self.settings.scopes)
        
        if "access_token" in result:
            self.logger.debug("Token acquired successfully")
            self._token_cache = result
            return result["access_token"]
        else:
            error_description = result.get("error_description", "Unknown error")
            self.logger.error(f"Failed to acquire token: {error_description}")
            return None
    
    def get_auth_header(self) -> Dict[str, str]:
        """
        Get authentication header for Graph API requests
        
        Returns:
            Dict[str, str]: Headers dictionary with Authorization header
        
        Raises:
            ValueError: If token acquisition fails
        """
        token = self.get_token()
        if not token:
            raise ValueError("Failed to acquire access token")
        
        return {"Authorization": f"Bearer {token}"}
    
    def _is_token_expired(self) -> bool:
        """
        Check if the cached token is expired
        
        Returns:
            bool: True if token is expired or about to expire, False otherwise
        """
        # For simplicity, we're not implementing actual expiry checking in this version
        # A proper implementation would check the expires_on field and compare with current time
        # For now, we'll always assume the token is expired if this method is called
        return True 