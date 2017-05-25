import json
from .reports import Reports

reports_list = []


def get_data(startDate, endDate, metric, count = 20):
    reports = Reports(reports_list)
    response = reports.data.batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': '149031868',
                    'dateRanges': [{'startDate':startDate, 'endDate': endDate}],
                    'metrics': [{'expression': 'ga:sessions'}],
                    'dimensions': [{"name": metric}],
                    'orderBys': [{"fieldName": "ga:sessions", "sortOrder": "DESCENDING"}],
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