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

    streamed = []
    raw_array = []

    def get_stations(self):
        header = self.HEADERS_COMMON.copy()
        header.update({
            'command': "list"
        })
        return json.loads(requests.request("POST", self.URLS['station'], headers=header).text)

    def rawdata_stream(self, start: datetime, end: datetime, step: timedelta):
        if end < start:
            raise Exception('End time should be not smaller than start time')

        def daterange(start_datetime, end_datetime):
            for n in range(int(((end_datetime - start_datetime).seconds + (end_datetime - start_datetime).days * 60*60*24) / (step.seconds + step.days * 60*60*24))):
                yield start_datetime + step * n

        for dt in daterange(start, end):
            self._get_one_rawdata(dt)
        return {
            'streamed': self.streamed,
            'raw': self.raw_array
        }

    def _get_one_rawdata(self, dt):
        time = dt.replace(microsecond=0).isoformat() + 'Z'
        if time not in self.streamed:
            header = self.HEADERS_COMMON.copy()

            header.update({
                'time_start': time,
                'time_stop': time
            })
            response = json.loads(requests.request("POST", self.URLS['raw'], headers=header).text)
            self.raw_array.extend(response['raw'])
            self.streamed.append(time)

            with open('rawdata_8', 'a') as file:
                file.write(str(response['raw']) + '\n')
