import json
from .reports import Reports

reports_list = []


def get_data(startDate, endDate, metric, count=None):
    reports = Reports(reports_list)
    response = reports.data.batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '142200509',
                    'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
                    # 'metrics': [{'expression': 'ga:sessions'}],
                    'metrics': [{'expression': 'ga:users'}],
                    'dimensions': [{"name": metric}],
                    # 'orderBys': [{"fieldName": "ga:sessions", "sortOrder": "DESCENDING"}],
                    'orderBys': [{"fieldName": "ga:users", "sortOrder": "DESCENDING"}],
                    'pageSize': count
                }]
        }
    ).execute()

        # read the response and extract the data we need
    for report in response.get('reports', []):
       # columnHeader = report.get('columnHeader', {})
       # dimensionHeaders = columnHeader.get('dimensions', [])
       # metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])
        return json.dumps(rows)
