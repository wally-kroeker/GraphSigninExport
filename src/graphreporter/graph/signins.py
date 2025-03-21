#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter Sign-In Logs Client
Client for retrieving sign-in logs from Microsoft Graph API
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Iterator

from graphreporter.graph.client import GraphClient


class SignInClient(GraphClient):
    """
    Client for retrieving sign-in logs from Microsoft Graph API
    
    Extends the base GraphClient with sign-in specific functionality
    """
    
    def __init__(self):
        """Initialize the sign-in logs client"""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        self.logger.debug("SignInClient initialized")
    
    def get_signins(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        user_id: Optional[str] = None,
        app_id: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Get sign-in logs from Microsoft Graph API
        
        Args:
            start_date: Start date for filtering logs
            end_date: End date for filtering logs
            user_id: Filter by user ID or userPrincipalName
            app_id: Filter by application ID
            max_results: Maximum number of results to return
            
        Returns:
            Iterator[Dict[str, Any]]: Iterator of sign-in log entries
        """
        self.logger.info(f"Retrieving sign-in logs")
        
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.now()
        if not start_date:
            start_date = end_date - timedelta(days=7)
        
        # Build filter string
        filter_parts = []
        
        # Date range filter
        start_str = start_date.isoformat() + "Z"
        end_str = end_date.isoformat() + "Z"
        filter_parts.append(f"createdDateTime ge {start_str} and createdDateTime le {end_str}")
        
        # User filter
        if user_id:
            filter_parts.append(f"userPrincipalName eq '{user_id}' or userId eq '{user_id}'")
        
        # App filter
        if app_id:
            filter_parts.append(f"appId eq '{app_id}'")
        
        # Combine filters
        filter_str = " and ".join(f"({part})" for part in filter_parts)
        
        # Query parameters
        params = {
            "$filter": filter_str,
            "$orderby": "createdDateTime desc",
        }
        
        # Add top parameter if max_results is specified
        if max_results:
            params["$top"] = str(max_results)
        
        self.logger.debug(f"Filter: {filter_str}")
        
        # Get paginated results
        count = 0
        for signin in self.get_paginated("auditLogs/signIns", params):
            if max_results and count >= max_results:
                break
            
            yield signin
            count += 1
        
        self.logger.info(f"Retrieved {count} sign-in logs")
    
    def get_signins_by_days(
        self,
        days: int,
        user_id: Optional[str] = None,
        app_id: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Get sign-in logs for the last N days
        
        Args:
            days: Number of days to look back
            user_id: Filter by user ID or userPrincipalName
            app_id: Filter by application ID
            max_results: Maximum number of results to return
            
        Returns:
            Iterator[Dict[str, Any]]: Iterator of sign-in log entries
        """
        self.logger.info(f"Retrieving sign-in logs for the last {days} days")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.get_signins(
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
            app_id=app_id,
            max_results=max_results,
        ) 