import json
import requests


class CMyHelsinki:
    url = "http://open-api.myhelsinki.fi/v1/events/"

    def get_events(self):
        response = json.loads(
            requests.request("GET", self.url).text)
        return json.dumps(response, indent=4, sort_keys=True)
