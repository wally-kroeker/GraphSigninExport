#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Applications Client
Client for retrieving app registration information from Microsoft Graph API
"""

import logging
from typing import Dict, List, Optional, Any, Iterator

from graphreporter.graph.client import GraphClient


class ApplicationsClient(GraphClient):
    """
    Client for retrieving app registration information from Microsoft Graph API
    
    Extends the base GraphClient with application-specific functionality
    """
    
    def __init__(self):
        """Initialize the applications client"""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        self.logger.debug("ApplicationsClient initialized")
    
    def get_applications(
        self,
        app_id: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        max_results: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Get app registrations from Microsoft Graph API
        
        Args:
            app_id: Filter by application ID
            permissions: Filter by required permission
            max_results: Maximum number of results to return
            
        Returns:
            Iterator[Dict[str, Any]]: Iterator of application objects
        """
        self.logger.info("Retrieving app registrations")
        
        # Build filter string
        filter_parts = []
        
        # App ID filter
        if app_id:
            filter_parts.append(f"appId eq '{app_id}'")
        
        # Combine filters
        params = {}
        if filter_parts:
            filter_str = " and ".join(f"({part})" for part in filter_parts)
            params["$filter"] = filter_str
            self.logger.debug(f"Filter: {filter_str}")
        
        # Select specific fields - add all the relevant fields for app registrations
        params["$select"] = "id,appId,displayName,createdDateTime,api,requiredResourceAccess,web,spa,publicClient"
        
        # Add top parameter if max_results is specified
        if max_results:
            params["$top"] = str(max_results)
        
        # Get paginated results
        count = 0
        for app in self.get_paginated("applications", params):
            # Post-filter for permissions if needed
            if permissions and not self._has_permissions(app, permissions):
                continue
                
            if max_results and count >= max_results:
                break
                
            yield app
            count += 1
        
        self.logger.info(f"Retrieved {count} app registrations")
    
    def _has_permissions(self, app: Dict[str, Any], permissions: List[str]) -> bool:
        """
        Check if an application has all the specified permissions
        
        Args:
            app: Application object
            permissions: List of permission identifiers to check for
            
        Returns:
            bool: True if the application has all the specified permissions, False otherwise
        """
        # Check if the app has required resource access
        if "requiredResourceAccess" not in app:
            return False
            
        # Flatten all resource accesses
        all_resource_accesses = []
        for resource in app["requiredResourceAccess"]:
            if "resourceAccess" in resource:
                all_resource_accesses.extend(resource["resourceAccess"])
        
        # Check if all permissions are in the resource accesses
        app_permission_ids = [access.get("id", "").lower() for access in all_resource_accesses]
        
        # For simplicity, just check if any permission string is in any of the access IDs or display names
        # In a real implementation, you would need to map permission names to IDs
        for permission in permissions:
            permission_lower = permission.lower()
            found = False
            
            # Check if the permission ID or name is in the app's permission IDs
            for app_permission in app_permission_ids:
                if permission_lower in app_permission:
                    found = True
                    break
            
            if not found:
                return False
        
        return True 