import asyncio
import argparse
from datetime import datetime, timedelta
import os
import csv
from graphreporter.auth.client import AuthClient
from graphreporter.reports.signin_logs import SignInLogsClient
from graphreporter.config.settings import Settings

async def export_chunk(signin_client, output_file, start_date, end_date, user_email, max_results=1000):
    """Export a chunk of sign-in logs for a specific user within a date range."""
    print(f"Exporting chunk from {start_date.date()} to {end_date.date()}...")
    
    result = await signin_client.export_to_csv(
        output_file=output_file,
        start_date=start_date,
        end_date=end_date,
        user_principal_name=user_email,
        max_results=max_results
    )
    
    return result

async def combine_csv_files(file_paths, output_file):
    """Combine multiple CSV files into one."""
    if not file_paths:
        return None
    
    if len(file_paths) == 1:
        return file_paths[0]
    
    print(f"Combining {len(file_paths)} CSV files into {output_file}...")
    
    # Read headers from the first file
    with open(file_paths[0], 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
    
    # Create a new combined file with the same headers
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(headers)
        
        # Copy data from each file, skipping headers
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as in_file:
                reader = csv.reader(in_file)
                next(reader)  # Skip header
                for row in reader:
                    writer.writerow(row)
    
    # Delete the individual chunk files
    for file_path in file_paths:
        os.remove(file_path)
    
    return output_file

async def main():
    """Export sign-in logs for a specific user."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export sign-in logs for a specific user.')
    parser.add_argument('user_email', help='Email address of the user to export logs for')
    parser.add_argument('--days', type=int, default=7, help='Number of days to look back (default: 7)')
    parser.add_argument('--chunk-days', type=int, default=3, help='Number of days per chunk to avoid timeouts (default: 3)')
    parser.add_argument('--no-combine', action='store_true', help='Do not combine chunk files into one')
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
    
    # Base output filename
    username = user_email.split("@")[0]
    base_output_file = os.path.join('exports', f'user_signin_logs_{username}_{start_date.date()}_{end_date.date()}.csv')
    
    print(f"Exporting sign-in logs for user '{user_email}' from {start_date.date()} to {end_date.date()}...")
    
    # Split the date range into chunks to avoid timeouts
    chunk_size = timedelta(days=args.chunk_days)
    chunk_files = []
    
    current_start = start_date
    chunk_number = 1
    
    while current_start < end_date:
        current_end = min(current_start + chunk_size, end_date)
        
        # Create a chunk filename
        chunk_file = os.path.join('exports', f'user_signin_logs_{username}_{current_start.date()}_{current_end.date()}_chunk{chunk_number}.csv')
        
        try:
            # Export the chunk
            result = await export_chunk(
                signin_client=signin_client,
                output_file=chunk_file,
                start_date=current_start,
                end_date=current_end,
                user_email=user_email,
                max_results=1000
            )
            
            if result:
                chunk_files.append(result)
                print(f"Successfully exported chunk {chunk_number} to: {result}")
                print(f"Chunk file size: {os.path.getsize(result)} bytes")
        except Exception as e:
            print(f"Error exporting chunk {chunk_number}: {str(e)}")
        
        # Move to the next chunk
        current_start = current_end
        chunk_number += 1
    
    # Combine chunks if needed
    final_file = base_output_file
    if chunk_files:
        if len(chunk_files) > 1 and not args.no_combine:
            final_file = await combine_csv_files(chunk_files, base_output_file)
        elif len(chunk_files) == 1:
            final_file = chunk_files[0]
            # Rename the file if it's different from the base output file
            if final_file != base_output_file:
                os.rename(final_file, base_output_file)
                final_file = base_output_file
    else:
        print(f"No sign-in logs found for user '{user_email}' in the specified period.")
        return
    
    print(f"Export completed. Final file: {final_file}")
    print(f"File size: {os.path.getsize(final_file)} bytes")
    
    # Count number of records and show which applications were used
    app_counts = {}
    with open(final_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            app_name = row.get('app_display_name', 'Unknown')
            app_counts[app_name] = app_counts.get(app_name, 0) + 1
    
    print(f"Number of sign-in records: {sum(app_counts.values())}")
    
    # Show application usage
    print("\nApplication usage summary:")
    for app, count in sorted(app_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {app}: {count} sign-ins")

if __name__ == "__main__":
    asyncio.run(main()) 