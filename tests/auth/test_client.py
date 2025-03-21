#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for GraphReporter Authentication Client
"""

import os
import pytest
from dotenv import load_dotenv

from graphreporter.auth.client import AuthClient
from graphreporter.config.settings import Settings

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def settings():
    """Create Settings instance for testing"""
    return Settings(
        tenant_id=os.getenv("GRAPH_TENANT_ID", ""),
        client_id=os.getenv("GRAPH_CLIENT_ID", ""),
        client_secret=os.getenv("GRAPH_CLIENT_SECRET", ""),
    )

@pytest.fixture
def auth_client(settings):
    """Create AuthClient instance for testing"""
    return AuthClient(settings)

@pytest.mark.asyncio
async def test_authentication(auth_client):
    """Test authentication with Microsoft Graph API"""
    # Skip test if credentials are not configured
    if not all([
        os.getenv("GRAPH_TENANT_ID"),
        os.getenv("GRAPH_CLIENT_ID"),
        os.getenv("GRAPH_CLIENT_SECRET")
    ]):
        pytest.skip("Microsoft Graph credentials not configured")
    
    # Test authentication
    assert await auth_client.test_authentication() is True 