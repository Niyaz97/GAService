import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2


class Reports:
    list = []

    def __init__(self, in_list):
        if in_list:
            self.data = in_list.pop()
        else:
            credentials = ServiceAccountCredentials.from_json_keyfile_name('api_key.json',
                                                               ['https://www.googleapis.com/auth/analytics.readonly'])
            service = build('analytics', 'v3', http=credentials.authorize(httplib2.Http()),
                discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))
            self.data = service.reports()
        self.list = in_list

    def __del__(self):
        self.list.append(self.data)
        self._print()

    def _print(self):
        print(' list has:')
        for line in self.list:
            print(line)