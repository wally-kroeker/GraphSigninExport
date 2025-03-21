#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for the authentication client
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient

from graphreporter.auth.client import AuthClient
from graphreporter.config.settings import Settings


class TestAuthClient:
    """Test cases for the AuthClient class"""
    
    def setup_method(self):
        """Set up test cases"""
        # Mock settings
        self.settings = MagicMock(spec=Settings)
        self.settings.tenant_id = "test-tenant-id"
        self.settings.client_id = "test-client-id"
        self.settings.client_secret = "test-client-secret"
        
        # Create auth client
        self.auth_client = AuthClient(self.settings)
    
    def test_credential_creation(self):
        """Test credential creation with correct parameters"""
        # Set up mock
        with patch('azure.identity.aio.ClientSecretCredential') as mock_credential:
            mock_credential_instance = MagicMock(spec=ClientSecretCredential)
            mock_credential.return_value = mock_credential_instance
            
            # Get credential property
            credential = self.auth_client.credential
            
            # Check credential creation with correct parameters
            mock_credential.assert_called_once_with(
                tenant_id="test-tenant-id",
                client_id="test-client-id",
                client_secret="test-client-secret"
            )
            
            # Check credential property returns the credential
            assert credential == mock_credential_instance
    
    def test_client_creation(self):
        """Test Graph client creation"""
        # Set up mocks
        with patch('azure.identity.aio.ClientSecretCredential') as mock_credential, \
             patch('msgraph.GraphServiceClient') as mock_graph_client:
            
            mock_credential_instance = MagicMock(spec=ClientSecretCredential)
            mock_credential.return_value = mock_credential_instance
            
            mock_client_instance = MagicMock(spec=GraphServiceClient)
            mock_graph_client.return_value = mock_client_instance
            
            # Get client
            client = self.auth_client.get_client()
            
            # Check client creation with correct parameters
            mock_graph_client.assert_called_once_with(
                credentials=mock_credential_instance,
                scopes=['https://graph.microsoft.com/.default']
            )
            
            # Check client is returned correctly
            assert client == mock_client_instance
    
    @pytest.mark.asyncio
    async def test_authentication_success(self):
        """Test successful authentication"""
        # Set up mocks
        with patch('azure.identity.aio.ClientSecretCredential') as mock_credential, \
             patch('msgraph.GraphServiceClient') as mock_graph_client:
            
            mock_credential_instance = MagicMock(spec=ClientSecretCredential)
            mock_credential.return_value = mock_credential_instance
            
            mock_client_instance = MagicMock(spec=GraphServiceClient)
            mock_org_response = MagicMock()
            mock_org_response.value = [{"id": "test-org"}]
            mock_client_instance.organization = MagicMock()
            mock_client_instance.organization.get = AsyncMock(return_value=mock_org_response)
            mock_graph_client.return_value = mock_client_instance
            
            # Test authentication
            result = await self.auth_client.test_authentication()
            
            # Check authentication was successful
            assert result is True
            mock_client_instance.organization.get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_authentication_failure(self):
        """Test authentication failure"""
        # Set up mocks
        with patch('azure.identity.aio.ClientSecretCredential') as mock_credential, \
             patch('msgraph.GraphServiceClient') as mock_graph_client:
            
            mock_credential_instance = MagicMock(spec=ClientSecretCredential)
            mock_credential.return_value = mock_credential_instance
            
            mock_client_instance = MagicMock(spec=GraphServiceClient)
            mock_client_instance.organization = MagicMock()
            mock_client_instance.organization.get = AsyncMock(side_effect=Exception("Authentication failed"))
            mock_graph_client.return_value = mock_client_instance
            
            # Test authentication
            result = await self.auth_client.test_authentication()
            
            # Check authentication failed
            assert result is False
            mock_client_instance.organization.get.assert_called_once() 