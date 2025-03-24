import asyncio
import argparse
from datetime import datetime, timedelta
import os
import csv
from graphreporter.auth.client import AuthClient
from graphreporter.reports.signin_logs import SignInLogsClient
from graphreporter.config.settings import Settings

async def export_chunk(signin_client, app_display_name, start_date, end_date, output_file):
    """Export logs for a specific timeframe."""
    try:
        print(f"Exporting sign-in logs from {start_date.date()} to {end_date.date()}...")
        result = await signin_client.export_to_csv(
            output_file=output_file,
            start_date=start_date,
            end_date=end_date,
            app_display_name=app_display_name,
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
    """Combine multiple CSV files into a single file, keeping only one header."""
    if not file_list:
        return None, 0
        
    total_rows = 0
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        for i, file_path in enumerate(file_list):
            if not os.path.exists(file_path):
                continue
                
            with open(file_path, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                
                # Write header only from the first file
                if i == 0:
                    header = next(reader)
                    writer.writerow(header)
                else:
                    next(reader)  # Skip header from other files
                
                # Write all rows
                for row in reader:
                    writer.writerow(row)
                    total_rows += 1
                    
            # Clean up individual chunk files
            os.remove(file_path)
            
    return output_file, total_rows

async def main():
    """Export sign-in logs for enterprise applications."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Export sign-in logs for enterprise applications.')
    parser.add_argument('app_name', help='The display name of the enterprise application')
    parser.add_argument('--days', type=int, default=7, help='Number of days to look back (default: 7)')
    parser.add_argument('--chunk-days', type=int, default=5, help='Number of days per chunk to avoid timeouts (default: 5)')
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
    
    app_display_name = args.app_name
    base_output_file = os.path.join('exports', f'enterprise_app_logs_{app_display_name}_{start_date.date()}_{end_date.date()}')
    
    # Break the date range into chunks
    chunk_files = []
    current_start = start_date
    chunk_number = 1
    
    while current_start < end_date:
        chunk_end = min(current_start + timedelta(days=args.chunk_days), end_date)
        chunk_file = f"{base_output_file}_chunk{chunk_number}.csv"
        
        count, result_file = await export_chunk(
            signin_client,
            app_display_name,
            current_start,
            chunk_end,
            chunk_file
        )
        
        if result_file:
            chunk_files.append(result_file)
            
        current_start = chunk_end
        chunk_number += 1
    
    # Combine chunks if requested
    if not args.no_combine and len(chunk_files) > 0:
        print("\nCombining chunk files...")
        final_file = f"{base_output_file}.csv"
        combined_file, total_rows = combine_csv_files(chunk_files, final_file)
        
        if combined_file:
            print(f"\nSuccessfully combined all chunks into: {combined_file}")
            print(f"Total number of records: {total_rows}")
        else:
            print("\nFailed to combine chunk files.")
    else:
        print("\nSkipping file combination as requested.")
        print("Individual chunk files are preserved in the exports directory.")

if __name__ == "__main__":
    asyncio.run(main()) 