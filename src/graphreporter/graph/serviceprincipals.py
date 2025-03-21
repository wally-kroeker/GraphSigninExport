#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Service Principals Client
Client for retrieving enterprise app (service principal) information from Microsoft Graph API
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Iterator

from graphreporter.graph.client import GraphClient


class ServicePrincipalsClient(GraphClient):
    """
    Client for retrieving service principal information from Microsoft Graph API
    
    Extends the base GraphClient with service principal-specific functionality
    """
    
    def __init__(self):
        """Initialize the service principals client"""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        self.logger.debug("ServicePrincipalsClient initialized")
    
    def get_service_principals(
        self,
        app_id: Optional[str] = None,
        created_after: Optional[datetime] = None,
        max_results: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Get service principals (enterprise apps) from Microsoft Graph API
        
        Args:
            app_id: Filter by application ID
            created_after: Filter by creation date
            max_results: Maximum number of results to return
            
        Returns:
            Iterator[Dict[str, Any]]: Iterator of service principal objects
        """
        self.logger.info("Retrieving service principals")
        
        # Build filter string
        filter_parts = []
        
        # App ID filter
        if app_id:
            filter_parts.append(f"appId eq '{app_id}'")
        
        # Creation date filter
        if created_after:
            created_str = created_after.isoformat() + "Z"
            filter_parts.append(f"createdDateTime ge {created_str}")
        
        # Combine filters
        params = {}
        if filter_parts:
            filter_str = " and ".join(f"({part})" for part in filter_parts)
            params["$filter"] = filter_str
            self.logger.debug(f"Filter: {filter_str}")
        
        # Select specific fields
        params["$select"] = "id,appId,displayName,appOwnerOrganizationId,createdDateTime,servicePrincipalType,oauth2PermissionScopes"
        
        # Add top parameter if max_results is specified
        if max_results:
            params["$top"] = str(max_results)
        
        # Get paginated results
        count = 0
        for sp in self.get_paginated("servicePrincipals", params):
            if max_results and count >= max_results:
                break
                
            yield sp
            count += 1
        
        self.logger.info(f"Retrieved {count} service principals")
    
    def get_service_principal_by_app_id(self, app_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific service principal by application ID
        
        Args:
            app_id: Application ID
            
        Returns:
            Optional[Dict[str, Any]]: Service principal object or None if not found
        """
        self.logger.info(f"Retrieving service principal for app ID: {app_id}")
        
        # Query parameters
        params = {
            "$filter": f"appId eq '{app_id}'",
            "$select": "id,appId,displayName,appOwnerOrganizationId,createdDateTime,servicePrincipalType,oauth2PermissionScopes"
        }
        
        # Get results
        try:
            response = self.get("servicePrincipals", params)
            results = response.get("value", [])
            
            if results:
                self.logger.debug(f"Found service principal for app ID: {app_id}")
                return results[0]
            else:
                self.logger.warning(f"No service principal found for app ID: {app_id}")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving service principal: {str(e)}")
            return None 