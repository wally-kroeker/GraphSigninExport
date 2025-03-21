#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter CLI Commands
Defines all the available CLI commands for the application
"""

from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console

# Placeholder imports for future implementation
# from graphreporter.auth.client import AuthClient
# from graphreporter.graph.signins import SignInClient
# from graphreporter.graph.applications import ApplicationsClient
# from graphreporter.graph.serviceprincipals import ServicePrincipalsClient
# from graphreporter.export.csv_exporter import CSVExporter
# from graphreporter.export.excel_exporter import ExcelExporter
# from graphreporter.export.json_exporter import JSONExporter

console = Console()

# Define output format enum
class OutputFormat(str, Enum):
    """Output format options"""
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"


# Sign-ins commands
signins_app = typer.Typer(help="Retrieve sign-in logs from Microsoft Graph API")

@signins_app.callback()
def signins_callback():
    """
    Retrieve sign-in logs from Microsoft Graph API.
    """
    pass


@signins_app.command("fetch")
def fetch_signins(
    last_days: Optional[int] = typer.Option(
        None, "--last-days", "-d", help="Fetch logs from the last N days"
    ),
    start_date: Optional[datetime] = typer.Option(
        None, "--start-date", "-s", help="Start date for sign-in logs (YYYY-MM-DD)"
    ),
    end_date: Optional[datetime] = typer.Option(
        None, "--end-date", "-e", help="End date for sign-in logs (YYYY-MM-DD)"
    ),
    user_id: Optional[str] = typer.Option(
        None, "--user-id", "-u", help="Filter by user ID or userPrincipalName"
    ),
    app_id: Optional[str] = typer.Option(
        None, "--app-id", "-a", help="Filter by application ID"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.CSV, "--format", "-f", help="Output format"
    ),
    output_dir: Optional[Path] = typer.Option(
        "./output", "--output-dir", "-o", help="Output directory"
    ),
):
    """
    Fetch sign-in logs from Microsoft Graph API.
    
    If --last-days is provided, it will override any start-date and end-date parameters.
    """
    console.print("[bold]Fetching sign-in logs...[/bold]")
    
    # Calculate date range if last_days is provided
    if last_days:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=last_days)
        console.print(f"Date range: [green]{start_date.date()}[/green] to [green]{end_date.date()}[/green]")
    elif start_date and end_date:
        console.print(f"Date range: [green]{start_date.date()}[/green] to [green]{end_date.date()}[/green]")
    else:
        console.print("[yellow]No date range specified. Using default of last 7 days.[/yellow]")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
    
    # TODO: Implement actual functionality
    console.print("[yellow]This feature is not yet implemented.[/yellow]")
    console.print(f"Output will be in [blue]{format.value}[/blue] format in [blue]{output_dir}[/blue]")


# App registrations commands
apps_app = typer.Typer(help="Retrieve app registrations from Microsoft Graph API")

@apps_app.callback()
def apps_callback():
    """
    Retrieve app registrations from Microsoft Graph API.
    """
    pass


@apps_app.command("list")
def list_apps(
    app_id: Optional[str] = typer.Option(
        None, "--app-id", "-a", help="Filter by application ID"
    ),
    permission: Optional[List[str]] = typer.Option(
        None, "--permission", "-p", help="Filter by permission"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.CSV, "--format", "-f", help="Output format"
    ),
    output_dir: Optional[Path] = typer.Option(
        "./output", "--output-dir", "-o", help="Output directory"
    ),
):
    """
    List app registrations from Microsoft Graph API.
    """
    console.print("[bold]Fetching app registrations...[/bold]")
    
    # TODO: Implement actual functionality
    console.print("[yellow]This feature is not yet implemented.[/yellow]")
    console.print(f"Output will be in [blue]{format.value}[/blue] format in [blue]{output_dir}[/blue]")


# Service principals commands
service_principals_app = typer.Typer(help="Retrieve service principals from Microsoft Graph API")

@service_principals_app.callback()
def service_principals_callback():
    """
    Retrieve service principals (enterprise apps) from Microsoft Graph API.
    """
    pass


@service_principals_app.command("list")
def list_service_principals(
    app_id: Optional[str] = typer.Option(
        None, "--app-id", "-a", help="Filter by application ID"
    ),
    created_after: Optional[datetime] = typer.Option(
        None, "--created-after", "-c", help="Filter by creation date (YYYY-MM-DD)"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.CSV, "--format", "-f", help="Output format"
    ),
    output_dir: Optional[Path] = typer.Option(
        "./output", "--output-dir", "-o", help="Output directory"
    ),
):
    """
    List service principals (enterprise apps) from Microsoft Graph API.
    """
    console.print("[bold]Fetching service principals...[/bold]")
    
    # TODO: Implement actual functionality
    console.print("[yellow]This feature is not yet implemented.[/yellow]")
    console.print(f"Output will be in [blue]{format.value}[/blue] format in [blue]{output_dir}[/blue]") 