from datetime import datetime, timedelta, date
from cstreamer import CStreamer
from ceventapi import CEventApi
import cstops
import cmyhelsinki
import json
import plotly.graph_objects as go
import plotly.express as px

import numpy as np

streamer = CStreamer()
sensors = streamer.get_station_locations()
# rawdata = streamer.get_rawdata(
#     start=datetime(2019, 8, 10, 0, 0, 0),
#     end=datetime(2019, 8, 17, 0, 0, 0),
#     step=timedelta(seconds=20),
#     filename='190810'
# )

# eventapi = CEventApi()
# events = eventapi.get_events(
#     start=datetime(2019, 11, 1, 0, 0, 0),
#     end=datetime(2019, 11, 30, 0, 0, 0)
# )
# print(events)
# places = eventapi.get_places()
# print(places)

# stopsapi = cstops.CStops()
# stops = stopsapi.get_stations()
# print(stops)

# f = open("events.txt", "w+")
# f.write(events)
# f.close()


# stopsapi = cstops.CStops()
# stops = stopsapi.get_nearest_station(60.45095, 25.01076)
# print(stops)


# eventsapi = cmyhelsinki.CMyHelsinki()
# events = eventsapi.get_events()
# print(events)
#
# f = open("myhelsinki_events.txt", "w+")
# f.write(events)
# f.close()


stopsapi = cstops.CStops()

stations = stopsapi.get_station_locations()

fig = go.Figure(go.Scattermapbox(
    mode="markers", marker=dict(size=10, color="magenta"),
    lon=stations['lon'], lat=stations['lat']))

stops = stopsapi.get_stations_tram()

fig.add_scattermapbox(lat=stops['lat'], lon=stops['lon'], mode="markers",
                      marker=dict(size=8, color="blue"))

fig.add_scattermapbox(lat=sensors['lat'], lon=sensors['lon'], mode="markers",
                      marker=dict(size=12, color="black"))


fig.add_scattermapbox(lon=[24.94], lat=[60.22], mode="markers", text=['próba'],
                      marker=dict(size=10, color="red"))

fig.update_layout(
    mapbox={
        'accesstoken': 'pk.eyJ1Ijoibm9yYmVydDg4IiwiYSI6ImNrMjgyY2Z4ZTF2dnQzYm16OXJmcDk3N3kifQ.BIt4mQU4oNObibeDEC7Yjg',
        'style': "open-street-map", 'zoom': 10, 'center': go.layout.mapbox.Center(lon=24.9471, lat=60.2202)},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False)

fig.show()
