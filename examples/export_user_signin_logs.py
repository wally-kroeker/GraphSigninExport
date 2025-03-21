import asyncio
import argparse
from datetime import datetime, timedelta
import os
from graphreporter.auth.client import AuthClient
from graphreporter.reports.signin_logs import SignInLogsClient
from graphreporter.config.settings import Settings

async def main():
    """Export sign-in logs for a specific user."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export sign-in logs for a specific user.')
    parser.add_argument('user_email', help='Email address of the user to export logs for')
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
    
    # Use the provided user email
    user_email = args.user_email
    
    output_file = os.path.join('exports', f'user_signin_logs_{user_email.split("@")[0]}_{start_date.date()}_{end_date.date()}.csv')
    
    print(f"Exporting sign-in logs for user '{user_email}' from {start_date.date()} to {end_date.date()}...")
    
    # Export the logs
    result = await signin_client.export_to_csv(
        output_file=output_file,
        start_date=start_date,
        end_date=end_date,
        user_principal_name=user_email,
        max_results=1000  # Adjust this number based on your needs
    )
    
    if result:
        print(f"Successfully exported sign-in logs to: {output_file}")
        print(f"File size: {os.path.getsize(output_file)} bytes")
        
        # Count number of records and show which applications were used
        app_counts = {}
        with open(result, 'r', encoding='utf-8') as f:
            import csv
            reader = csv.DictReader(f)
            for row in reader:
                app_name = row.get('app_display_name', 'Unknown')
                app_counts[app_name] = app_counts.get(app_name, 0) + 1
        
        print(f"Number of sign-in records: {sum(app_counts.values())}")
        
        # Show application usage
        print("\nApplication usage summary:")
        for app, count in sorted(app_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {app}: {count} sign-ins")
    else:
        print(f"No sign-in logs found for user '{user_email}' in the specified period.")

if __name__ == "__main__":
    asyncio.run(main()) 