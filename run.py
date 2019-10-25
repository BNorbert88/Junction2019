from datetime import datetime
from cstreamer import CStreamer


streamer = CStreamer()
stations = streamer.get_stations()
raw = streamer.get_rawdata(start=datetime(2019, 7, 15, 0, 0, 0), end=datetime(2019, 7, 15, 0, 1, 0))

streamed = []

print(raw)
