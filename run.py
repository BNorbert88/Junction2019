from datetime import datetime, timedelta, date
from cstreamer import CStreamer
from ceventapi import CEventApi

import numpy as np

# streamer = CStreamer()
# stations = streamer.get_stations()
# rawdata = streamer.get_rawdata(
#     start=datetime(2019, 8, 10, 0, 0, 0),
#     end=datetime(2019, 8, 17, 0, 0, 0),
#     step=timedelta(seconds=20),
#     filename='190810'
# )

eventapi = CEventApi()
events = eventapi.get_events(
    start=datetime(2019, 8, 10, 0, 0, 0),
    end=datetime(2019, 8, 16, 0, 0, 0)
)
# print(events)
places = eventapi.get_places()
# print(places)
