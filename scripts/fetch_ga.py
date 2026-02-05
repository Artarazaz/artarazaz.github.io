import os
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

def fetch_visitor_count(property_id):
    """Fetches the total users from GA4."""
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="year")], # Dummy dimension
        metrics=[Metric(name="totalUsers")],
        date_ranges=[DateRange(start_date="2024-01-01", end_date="today")],
    )
    
    response = client.run_report(request)
    
    total_users = 0
    if response.rows:
        total_users = sum(int(row.metric_values[0].value) for row in response.rows)
    
    return total_users

if __name__ == "__main__":
    PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")
    if not PROPERTY_ID:
        print("Error: GA4_PROPERTY_ID not set.")
        exit(1)

    try:
        count = fetch_visitor_count(PROPERTY_ID)
        data = {"total_visits": count}
        
        with open("visitor-data.json", "w") as f:
            json.dump(data, f)
        
        print(f"Successfully updated visitor-data.json with {count} visits.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
