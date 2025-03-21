#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for the authentication client
"""

import unittest
from unittest.mock import patch, MagicMock

from graphreporter.auth.client import AuthClient


class TestAuthClient(unittest.TestCase):
    """Test cases for the AuthClient class"""
    
    @patch('graphreporter.auth.client.get_settings')
    def setUp(self, mock_get_settings):
        """Set up test cases"""
        # Mock settings
        mock_settings = MagicMock()
        mock_settings.tenant_id = "test-tenant-id"
        mock_settings.client_id = "test-client-id"
        mock_settings.client_secret = "test-client-secret"
        mock_settings.authority_url = "https://login.microsoftonline.com/test-tenant-id"
        mock_settings.scopes = ["https://graph.microsoft.com/.default"]
        
        mock_get_settings.return_value = mock_settings
        
        # Create auth client
        self.auth_client = AuthClient()
    
    @patch('msal.ConfidentialClientApplication')
    def test_app_creation(self, mock_msal_app):
        """Test app creation with correct parameters"""
        # Set up mock
        mock_app_instance = MagicMock()
        mock_msal_app.return_value = mock_app_instance
        
        # Get app property
        app = self.auth_client.app
        
        # Check MSAL app creation with correct parameters
        mock_msal_app.assert_called_once_with(
            client_id="test-client-id",
            client_credential="test-client-secret",
            authority="https://login.microsoftonline.com/test-tenant-id",
        )
        
        # Check app property returns the MSAL app
        self.assertEqual(app, mock_app_instance)
    
    @patch('msal.ConfidentialClientApplication')
    def test_get_token(self, mock_msal_app):
        """Test token acquisition"""
        # Set up mock
        mock_app_instance = MagicMock()
        mock_app_instance.acquire_token_for_client.return_value = {
            "access_token": "test-access-token",
            "expires_in": 3600,
        }
        mock_msal_app.return_value = mock_app_instance
        
        # Get token
        token = self.auth_client.get_token()
        
        # Check token acquisition with correct scopes
        mock_app_instance.acquire_token_for_client.assert_called_once_with(
            scopes=["https://graph.microsoft.com/.default"]
        )
        
        # Check token is returned correctly
        self.assertEqual(token, "test-access-token")
    
    @patch('msal.ConfidentialClientApplication')
    def test_get_auth_header(self, mock_msal_app):
        """Test auth header generation"""
        # Set up mock
        mock_app_instance = MagicMock()
        mock_app_instance.acquire_token_for_client.return_value = {
            "access_token": "test-access-token",
            "expires_in": 3600,
        }
        mock_msal_app.return_value = mock_app_instance
        
        # Get auth header
        header = self.auth_client.get_auth_header()
        
        # Check auth header is correct
        self.assertEqual(header, {"Authorization": "Bearer test-access-token"})
    
    @patch('msal.ConfidentialClientApplication')
    def test_get_token_failure(self, mock_msal_app):
        """Test token acquisition failure"""
        # Set up mock
        mock_app_instance = MagicMock()
        mock_app_instance.acquire_token_for_client.return_value = {
            "error": "unauthorized_client",
            "error_description": "AADSTS700016: Application with identifier 'test-client-id' was not found in the directory.",
        }
        mock_msal_app.return_value = mock_app_instance
        
        # Get token
        token = self.auth_client.get_token()
        
        # Check token is None
        self.assertIsNone(token)
    
    @patch('msal.ConfidentialClientApplication')
    def test_get_auth_header_failure(self, mock_msal_app):
        """Test auth header generation with token acquisition failure"""
        # Set up mock
        mock_app_instance = MagicMock()
        mock_app_instance.acquire_token_for_client.return_value = {
            "error": "unauthorized_client",
            "error_description": "AADSTS700016: Application with identifier 'test-client-id' was not found in the directory.",
        }
        mock_msal_app.return_value = mock_app_instance
        
        # Get auth header should raise ValueError
        with self.assertRaises(ValueError):
            self.auth_client.get_auth_header()


if __name__ == '__main__':
    unittest.main() 