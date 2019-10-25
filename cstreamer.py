import requests
import json
from datetime import datetime, timedelta


class CStreamer:
    HEADERS_COMMON = {
        'x-api-key': "iQ0WKQlv3a7VqVSKG6BlE9IQ88bUYQws6UZLRs1B",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "api.hypr.cl",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "0",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    URLS = {
        'raw': "https://api.hypr.cl/raw/",
        'station': "https://api.hypr.cl/station/"
    }

    def get_stations(self):
        header = self.HEADERS_COMMON.copy()
        header.update({
            'command': "list"
        })
        return json.loads(requests.request("POST", self.URLS['station'], headers=header).text)

    def get_rawdata(self, start: datetime, end: datetime):
        if end < start:
            raise Exception('End time should be not smaller than start time')

        def daterange(start_datetime, end_datetime):
            for n in range(int((end_datetime - start_datetime).seconds)):
                yield start_datetime + timedelta(seconds=n)

        raw_array = []
        for dt in daterange(start, end):
            header = self.HEADERS_COMMON.copy()
            header.update({
                'time_start': dt.replace(microsecond=0).isoformat()+'Z',
                'time_stop': dt.replace(microsecond=0).isoformat()+'Z'
            })
            response = json.loads(requests.request("POST", self.URLS['raw'], headers=header).text)
            raw_array.extend(response['raw'])
        return raw_array
