import os
from datetime import datetime, timedelta
import pytest
from graphreporter.auth.client import AuthClient
from graphreporter.reports.signin_logs import SignInLogsClient
from graphreporter.config.settings import Settings

@pytest.mark.asyncio
async def test_signin_logs_retrieval():
    """Test retrieving sign-in logs."""
    settings = Settings()
    auth_client = AuthClient(settings)
    graph_client = auth_client.get_client()
    
    signin_client = SignInLogsClient(graph_client)
    
    # Get logs for the last 7 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    logs = await signin_client.get_signin_logs(
        start_date=start_date,
        end_date=end_date,
        max_results=10
    )
    
    assert logs is not None
    assert isinstance(logs, list)
    if logs:  # If there are any logs
        assert isinstance(logs[0], dict)
        assert 'id' in logs[0]
        assert 'created_datetime' in logs[0]
        assert 'user_display_name' in logs[0]

@pytest.mark.asyncio
async def test_signin_logs_export():
    """Test exporting sign-in logs to CSV."""
    settings = Settings()
    auth_client = AuthClient(settings)
    graph_client = auth_client.get_client()
    
    signin_client = SignInLogsClient(graph_client)
    
    # Get logs for the last 7 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    output_file = "test_signin_logs.csv"
    
    try:
        result = await signin_client.export_to_csv(
            output_file=output_file,
            start_date=start_date,
            end_date=end_date,
            max_results=10
        )
        
        if result:  # If there were logs to export
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0
            
            # Read the first line to verify headers
            with open(output_file, 'r', encoding='utf-8') as f:
                headers = f.readline().strip().split(',')
                assert 'id' in headers
                assert 'created_datetime' in headers
                assert 'user_display_name' in headers
    finally:
        # Clean up the test file
        if os.path.exists(output_file):
            os.remove(output_file) 