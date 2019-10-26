from datetime import datetime, timedelta, date
from cstreamer import CStreamer
from ceventapi import CEventApi
import cstops
import cmyhelsinki
import json
import plotly.graph_objects as go

import numpy as np

# streamer = CStreamer()
# stations = streamer.get_stations()
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

import plotly.express as px

stopsapi = cstops.CStops()
#
stations = stopsapi.get_station_locations()
#
# fig = px.scatter_mapbox(stations, lat="lat", lon="lon", hover_name="name", hover_data=["name"],
#                         color_discrete_sequence=["fuchsia"], zoom=10, height=600)
#
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#
# fig.show()

fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = stations['lon'], lat = stations['lat']))

# fig.add_scatter(x=stations['lat'],y = stations['lon'], mode="lines",
#                 marker=dict(size=20, color="LightSeaGreen"))

fig.update_layout(
    mapbox = {
        'accesstoken': 'pk.eyJ1Ijoibm9yYmVydDg4IiwiYSI6ImNrMjgyY2Z4ZTF2dnQzYm16OXJmcDk3N3kifQ.BIt4mQU4oNObibeDEC7Yjg',
        'style': "open-street-map", 'zoom': 10, 'center': go.layout.mapbox.Center(lon=24.9471, lat=60.2202)},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend = False)



fig.show()

