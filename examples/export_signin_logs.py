import asyncio
from datetime import datetime, timedelta
import os
from graphreporter.auth.client import AuthClient
from graphreporter.reports.signin_logs import SignInLogsClient
from graphreporter.config.settings import Settings

async def main():
    """Export sign-in logs for the last 7 days."""
    # Initialize the settings and auth client
    settings = Settings()
    auth_client = AuthClient(settings)
    graph_client = auth_client.get_client()
    
    # Create the sign-in logs client
    signin_client = SignInLogsClient(graph_client)
    
    # Set the date range for the last 7 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    # Create the output directory if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    output_file = os.path.join('exports', f'signin_logs_{start_date.date()}_{end_date.date()}.csv')
    
    print(f"Exporting sign-in logs from {start_date.date()} to {end_date.date()}...")
    
    # Export the logs
    result = await signin_client.export_to_csv(
        output_file=output_file,
        start_date=start_date,
        end_date=end_date,
        max_results=1000  # Adjust this number based on your needs
    )
    
    if result:
        print(f"Successfully exported sign-in logs to: {output_file}")
        print(f"File size: {os.path.getsize(output_file)} bytes")
    else:
        print("No sign-in logs found for the specified period.")

if __name__ == "__main__":
    asyncio.run(main()) 