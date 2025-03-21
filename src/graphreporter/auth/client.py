#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Authentication Client
Handles authentication with Microsoft Graph API using azure-identity
"""

import logging
from typing import Optional

from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient

from graphreporter.config.settings import Settings


class AuthClient:
    """
    Authentication client for Microsoft Graph API using client credentials flow
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize the authentication client
        
        Args:
            settings: Application settings containing credentials
        """
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self._credential: Optional[ClientSecretCredential] = None
        self._client: Optional[GraphServiceClient] = None
        
        self.logger.debug("AuthClient initialized")
    
    @property
    def credential(self) -> ClientSecretCredential:
        """
        Get or create the ClientSecretCredential
        
        Returns:
            ClientSecretCredential: The credential object
        """
        if not self._credential:
            self.logger.debug("Creating ClientSecretCredential")
            self._credential = ClientSecretCredential(
                tenant_id=self.settings.tenant_id,
                client_id=self.settings.client_id,
                client_secret=self.settings.client_secret
            )
        return self._credential
    
    def get_client(self) -> GraphServiceClient:
        """
        Get or create the GraphServiceClient
        
        Returns:
            GraphServiceClient: The client object
        """
        if not self._client:
            self.logger.debug("Creating GraphServiceClient")
            self._client = GraphServiceClient(
                credentials=self.credential,
                scopes=['https://graph.microsoft.com/.default']
            )
        return self._client
    
    async def test_authentication(self) -> bool:
        """
        Test the authentication by making a simple Graph API call
        
        Returns:
            bool: True if authentication is successful, False otherwise
        """
        try:
            client = self.get_client()
            # Try to get the organization details as a test
            result = await client.organization.get()
            return bool(result and result.value)
        except Exception as e:
            self.logger.error(f"Authentication test failed: {e}")
            return False 