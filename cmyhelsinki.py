import json
import urllib

import requests


class CMyHelsinki:
    url = "http://open-api.myhelsinki.fi/v1/events/"
    url2 = "http://open-api.myhelsinki.fi/v1/event/"

    def get_events(self):
        response = json.loads(
            requests.request("GET", self.url).text)
        return response

    def get_specific_event(self, event_id):
        response = json.loads(
            requests.request("GET", self.url2+urllib.parse.quote(event_id)).text)
        return response
