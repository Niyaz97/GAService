from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import httplib2


class Reports:
    def __init__(self, list):
        if list:
            self.data = list.pop()
        else:
            credentials = ServiceAccountCredentials.from_json_keyfile_name('api_key.json',
                                                               ['https://www.googleapis.com/auth/analytics.readonly'])
            self.data = build('analytics', 'v4', http=credentials.authorize(httplib2.Http()),
                discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest')).reports()

        self.list = list

    def __del__(self):
        self.list.append(self.data)
        self._print()

    def _print(self):
        print(' list has:')
        for line in self.list:
            print(line)
