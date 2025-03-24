import asyncio
from datetime import datetime, timedelta
import os
import argparse
from graphreporter.auth.client import AuthClient
from graphreporter.reports.signin_logs import SignInLogsClient
from graphreporter.config.settings import Settings

async def main():
    """Export sign-in logs for enterprise applications."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export sign-in logs for enterprise applications.')
    parser.add_argument('app_name', help='The display name of the enterprise application')
    parser.add_argument('--days', type=int, default=7, help='Number of days to look back (default: 7)')
    args = parser.parse_args()

    # Initialize the settings and auth client
    settings = Settings()
    auth_client = AuthClient(settings)
    graph_client = auth_client.get_client()
    
    # Create the sign-in logs client
    signin_client = SignInLogsClient(graph_client)
    
    # Set the date range based on the days argument
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=args.days)
    
    # Create the output directory if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    
    app_display_name = args.app_name
    
    output_file = os.path.join('exports', f'enterprise_app_logs_{app_display_name}_{start_date.date()}_{end_date.date()}.csv')
    
    print(f"Exporting sign-in logs for application '{app_display_name}' from {start_date.date()} to {end_date.date()}...")
    
    # Export the logs
    result = await signin_client.export_to_csv(
        output_file=output_file,
        start_date=start_date,
        end_date=end_date,
        app_display_name=app_display_name,
        max_results=1000  # Adjust this number based on your needs
    )
    
    if result:
        print(f"Successfully exported sign-in logs to: {output_file}")
        print(f"File size: {os.path.getsize(output_file)} bytes")
        
        # Count number of records
        with open(result, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f) - 1  # Subtract 1 for the header row
        print(f"Number of sign-in records: {line_count}")
    else:
        print("Failed to export sign-in logs.")

if __name__ == "__main__":
    asyncio.run(main()) 