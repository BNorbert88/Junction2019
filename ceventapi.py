import requests
import json
from datetime import datetime


class CEventApi:
    HEADERS_COMMON = {
        'x-api-key': "iQ0WKQlv3a7VqVSKG6BlE9IQ88bUYQws6UZLRs1B",
        'Accept': "application/json; utf-8",
        'Cache-Control': "no-cache",
        'Host': "api.hel.fi",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "0",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    # URL = "http://api.hel.fi/linkedevents/v1/?format=api"
    URLS = {
        'events': "http://api.hel.fi/linkedevents/v1/event/?include=location,keywords&",
        'places': "http://api.hel.fi/linkedevents/v1/place/?"
    }

    def get_events(self, start: datetime, end: datetime):
        url = self.URLS['events']
        url += "start=" + str(start) + "&end=" + str(end)
        response = json.loads(requests.request("GET", url, headers=self.HEADERS_COMMON).text)
        return response

    def get_places(self):
        response = json.loads(requests.request("GET", self.URLS['places'], headers=self.HEADERS_COMMON).text)
        return response
