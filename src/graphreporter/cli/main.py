#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphReporter CLI
Main CLI interface using Typer
"""

import sys
from typing import Optional

import typer
from rich.console import Console

from graphreporter.cli import commands
from graphreporter import __version__

app = typer.Typer(
    name="graphreporter",
    help="Microsoft Graph Reporting Tool for Azure AD",
    add_completion=False,
)

console = Console()

# Add commands to the app
app.add_typer(commands.signins_app, name="fetch-signins")
app.add_typer(commands.apps_app, name="list-apps")
app.add_typer(commands.service_principals_app, name="list-service-principals")


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", help="Show the application version and exit."
    ),
) -> None:
    """
    Microsoft Graph Reporting Tool for Azure AD.
    
    Retrieve and export data from Microsoft Entra ID (Azure AD) using Microsoft Graph API.
    """
    if version:
        console.print(f"GraphReporter Version: {__version__}")
        raise typer.Exit()


def main() -> None:
    """
    Main entry point for the CLI application
    """
    try:
        app()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 