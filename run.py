from datetime import datetime, timedelta
from cstreamer import CStreamer

import numpy as np

streamer = CStreamer()
stations = streamer.get_stations()
rawdata = streamer.rawdata_stream(
    start=datetime(2019, 8, 5, 0, 0, 0),
    end=datetime(2019, 8, 6, 0, 0, 0),
    step=timedelta(seconds=120))
