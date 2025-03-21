from datetime import datetime
from typing import List, Optional

from msgraph import GraphServiceClient
from msgraph.generated.audit_logs.sign_ins.sign_ins_request_builder import SignInsRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration

class SignInLogsClient:
    """Client for retrieving and processing sign-in logs from Microsoft Graph."""

    def __init__(self, graph_client: GraphServiceClient):
        """Initialize the SignInLogsClient.
        
        Args:
            graph_client: An authenticated GraphServiceClient instance
        """
        self.graph_client = graph_client

    async def get_signin_logs(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        app_id: Optional[str] = None,
        app_display_name: Optional[str] = None,
        user_principal_name: Optional[str] = None,
        max_results: Optional[int] = None
    ) -> List[dict]:
        """Retrieve sign-in logs based on specified filters.
        
        Args:
            start_date: Optional start date for filtering logs
            end_date: Optional end date for filtering logs
            app_id: Optional application ID to filter logs
            app_display_name: Optional application display name to filter logs
            user_principal_name: Optional user email to filter logs
            max_results: Optional maximum number of results to return
            
        Returns:
            List of sign-in log entries
        """
        filter_conditions = []
        
        if start_date:
            filter_conditions.append(
                f"createdDateTime ge {start_date.isoformat()}Z"
            )
        if end_date:
            filter_conditions.append(
                f"createdDateTime le {end_date.isoformat()}Z"
            )
        if app_id:
            filter_conditions.append(f"appId eq '{app_id}'")
        if app_display_name:
            filter_conditions.append(f"appDisplayName eq '{app_display_name}'")
        if user_principal_name:
            filter_conditions.append(f"userPrincipalName eq '{user_principal_name}'")

        filter_string = " and ".join(filter_conditions) if filter_conditions else None

        query_params = SignInsRequestBuilder.SignInsRequestBuilderGetQueryParameters(
            filter=filter_string,
            top=max_results
        )

        request_configuration = RequestConfiguration(
            query_parameters=query_params
        )

        result = await self.graph_client.audit_logs.sign_ins.get(
            request_configuration=request_configuration
        )

        # Convert to list of dicts for easier processing
        logs = []
        if result and hasattr(result, 'value'):
            for log in result.value:
                log_dict = {
                    'id': log.id,
                    'created_datetime': log.created_date_time,
                    'user_display_name': log.user_display_name,
                    'user_principal_name': log.user_principal_name,
                    'user_id': log.user_id,
                    'app_id': log.app_id,
                    'app_display_name': log.app_display_name,
                    'ip_address': log.ip_address,
                    'client_app_used': log.client_app_used,
                    'status': {
                        'error_code': log.status.error_code if log.status else None,
                        'failure_reason': log.status.failure_reason if log.status else None
                    },
                    'location': {
                        'city': log.location.city if log.location else None,
                        'state': log.location.state if log.location else None,
                        'country_or_region': log.location.country_or_region if log.location else None
                    },
                    'device_detail': {
                        'browser': log.device_detail.browser if log.device_detail else None,
                        'operating_system': log.device_detail.operating_system if log.device_detail else None
                    }
                }
                logs.append(log_dict)

        return logs

    async def export_to_csv(
        self,
        output_file: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        app_id: Optional[str] = None,
        app_display_name: Optional[str] = None,
        user_principal_name: Optional[str] = None,
        max_results: Optional[int] = None
    ) -> str:
        """Export sign-in logs to a CSV file.
        
        Args:
            output_file: Path to the output CSV file
            start_date: Optional start date for filtering logs
            end_date: Optional end date for filtering logs
            app_id: Optional application ID to filter logs
            app_display_name: Optional application display name to filter logs
            user_principal_name: Optional user email to filter logs
            max_results: Optional maximum number of results to return
            
        Returns:
            Path to the created CSV file
        """
        import csv
        import json

        logs = await self.get_signin_logs(
            start_date=start_date,
            end_date=end_date,
            app_id=app_id,
            app_display_name=app_display_name,
            user_principal_name=user_principal_name,
            max_results=max_results
        )

        if not logs:
            return None

        # Flatten nested dictionaries for CSV export
        flattened_logs = []
        for log in logs:
            flat_log = {
                'id': log['id'],
                'created_datetime': log['created_datetime'],
                'user_display_name': log['user_display_name'],
                'user_principal_name': log['user_principal_name'],
                'user_id': log['user_id'],
                'app_id': log['app_id'],
                'app_display_name': log['app_display_name'],
                'ip_address': log['ip_address'],
                'client_app_used': log['client_app_used'],
                'status_error_code': log['status']['error_code'],
                'status_failure_reason': log['status']['failure_reason'],
                'location_city': log['location']['city'],
                'location_state': log['location']['state'],
                'location_country_or_region': log['location']['country_or_region'],
                'device_browser': log['device_detail']['browser'],
                'device_operating_system': log['device_detail']['operating_system']
            }
            flattened_logs.append(flat_log)

        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if not flattened_logs:
                return None
                
            writer = csv.DictWriter(f, fieldnames=flattened_logs[0].keys())
            writer.writeheader()
            writer.writerows(flattened_logs)

        return output_file 