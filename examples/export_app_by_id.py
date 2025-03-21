import asyncio
import argparse
from datetime import datetime, timedelta
import os
import sys
import csv
from graphreporter.auth.client import AuthClient
from graphreporter.reports.signin_logs import SignInLogsClient
from graphreporter.config.settings import Settings

async def export_for_timeframe(signin_client, app_id, start_date, end_date, output_file):
    """Export logs for a specific timeframe."""
    try:
        print(f"Exporting sign-in logs from {start_date.date()} to {end_date.date()}...")
        result = await signin_client.export_to_csv(
            output_file=output_file,
            start_date=start_date,
            end_date=end_date,
            app_id=app_id,
            max_results=1000  # Maximum allowed by API in a single call
        )
        
        if result:
            print(f"Successfully exported to: {output_file}")
            print(f"File size: {os.path.getsize(output_file)} bytes")
            
            # Count number of records
            with open(result, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f) - 1  # Subtract 1 for the header row
            print(f"Number of sign-in records: {line_count}")
            return line_count, result
        else:
            print(f"No sign-in logs found for this period.")
            return 0, None
    except Exception as e:
        print(f"Error exporting logs: {str(e)}")
        print(f"Try using a smaller time window or check your connection.")
        return 0, None

def combine_csv_files(file_list, output_file):
    """Combine multiple CSV files into a single file, keeping only one header.
    
    Args:
        file_list: List of CSV files to combine
        output_file: Path to the output combined CSV file
        
    Returns:
        Path to the combined file and the total number of rows
    """
    if not file_list:
        return None, 0
    
    # Sort files by date (assuming filename format includes dates)
    file_list.sort()
    
    total_rows = 0
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        # Process the first file - keep its header
        with open(file_list[0], 'r', encoding='utf-8') as firstfile:
            reader = csv.reader(firstfile)
            writer = csv.writer(outfile)
            
            # Copy header from first file
            header = next(reader)
            writer.writerow(header)
            
            # Copy data from first file
            for row in reader:
                writer.writerow(row)
                total_rows += 1
        
        # Process all other files - skip their headers
        for file_path in file_list[1:]:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                
                # Skip header
                next(reader, None)
                
                # Copy data
                for row in reader:
                    writer.writerow(row)
                    total_rows += 1
    
    return output_file, total_rows

async def main(app_id, days=90, chunk_days=10, combine=True):
    """Export sign-in logs for an application identified by its ID.
    
    Args:
        app_id: The application ID to filter logs by
        days: Number of days to look back for logs (default: 90)
        chunk_days: Number of days per query chunk to avoid timeouts (default: 10)
        combine: Whether to combine all CSV files into one (default: True)
    """
    # Initialize the settings and auth client
    settings = Settings()
    auth_client = AuthClient(settings)
    graph_client = auth_client.get_client()
    
    # Create the sign-in logs client
    signin_client = SignInLogsClient(graph_client)
    
    # Create the output directory if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    
    # Calculate date ranges
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Break the query into smaller time chunks to avoid timeouts
    total_records = 0
    all_files = []
    
    current_end = end_date
    current_start = max(end_date - timedelta(days=chunk_days), start_date)
    
    # Fix the loop condition to avoid infinite loops
    while current_start > start_date or (current_start == start_date and current_end > current_start):
        # Create unique filename for each chunk
        chunk_output_file = os.path.join(
            'exports', 
            f'app_signin_logs_{app_id}_{current_start.date()}_{current_end.date()}.csv'
        )
        
        # Export logs for this time chunk
        chunk_records, chunk_file = await export_for_timeframe(
            signin_client, app_id, current_start, current_end, chunk_output_file
        )
        
        if chunk_file:
            total_records += chunk_records
            all_files.append(chunk_file)
        
        # Move to the next time chunk
        current_end = current_start - timedelta(seconds=1)
        current_start = max(current_start - timedelta(days=chunk_days), start_date)
        
        # Break if we're going to process the same dates again
        if current_start == start_date and current_end <= start_date:
            break
    
    print(f"\nExport summary:")
    print(f"Total records exported: {total_records}")
    print(f"Files created: {len(all_files)}")
    
    # Combine files if requested and if we have multiple files
    if combine and len(all_files) > 1:
        combined_file = os.path.join(
            'exports',
            f'app_signin_logs_{app_id}_{start_date.date()}_{end_date.date()}_combined.csv'
        )
        
        print(f"\nCombining files into a single CSV file...")
        result_file, row_count = combine_csv_files(all_files, combined_file)
        
        if result_file:
            print(f"Successfully combined files into: {result_file}")
            print(f"Combined file size: {os.path.getsize(result_file)} bytes")
            print(f"Total rows in combined file: {row_count}")
        else:
            print("Failed to combine files.")
    elif len(all_files) > 1:
        print(f"\nMultiple files were created due to the time range. If you want to combine them manually:")
        print(f"1. The files contain headers, so you'll need to remove duplicate headers when combining")
        print(f"2. Use a tool like Excel to merge the CSV files")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export sign-in logs for a specific application ID")
    parser.add_argument("app_id", help="The application ID to filter logs by")
    parser.add_argument("--days", type=int, default=90, 
                        help="Number of days to look back for logs (default: 90)")
    parser.add_argument("--chunk-days", type=int, default=10, 
                        help="Number of days per query chunk to avoid timeouts (default: 10)")
    parser.add_argument("--no-combine", action="store_true",
                        help="Do not combine multiple CSV files into one")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(main(args.app_id, args.days, args.chunk_days, not args.no_combine))
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1) 