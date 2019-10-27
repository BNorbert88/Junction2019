import urllib
from datetime import datetime, timedelta, date
from cstreamer import CStreamer
from ceventapi import CEventApi
import cstops
import cmyhelsinki
import json
import openrouteservice
import plotly.graph_objects as go
import plotly.express as px
from openrouteservice import convert

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


#########################################xx

def knn1(vek, mtx, k, kd=1000):
    l = len(mtx[:, 0])
    outind = np.zeros(k) - 1
    outdis = np.zeros(k) + kd

    for i in range(l):

        tav = np.sqrt(np.sum((vek - mtx[i, :]) * (vek - mtx[i, :])))

        tolas = 0
        tolin = 0
        toldi = 0
        for j in range(k):
            if tolas == 0:
                if tav < outdis[j]:
                    tolin = outind[j]
                    toldi = outdis[j]
                    tolas = 1
                    outind[j] = i
                    outdis[j] = tav
            else:
                temp = outind[j]
                outind[j] = tolin
                tolin = temp
                temp = outdis[j]
                outdis[j] = toldi
                toldi = temp

    return (outind, outdis)


def knn2(vek, mtx, k, distvek, maxdist=0, kd=1000):
    l = len(mtx[:, 0])
    outind = np.zeros(k) - 1
    outdis = np.zeros(k) + kd

    for i in range(l):

        tav = np.sqrt(np.sum((vek - mtx[i, :]) * (vek - mtx[i, :])))
        if (maxdist > 0):
            if distvek[i] > maxdist:
                continue

        if maxdist == 0:
            tav = tav * distvek[i] * 100

        tolas = 0
        tolin = 0
        toldi = 0
        for j in range(k):
            if tolas == 0:
                if tav < outdis[j]:
                    tolin = outind[j]
                    toldi = outdis[j]
                    tolas = 1
                    outind[j] = i
                    outdis[j] = tav
            else:
                temp = outind[j]
                outind[j] = tolin
                tolin = temp
                temp = outdis[j]
                outdis[j] = toldi
                toldi = temp

    return (outind, outdis)


f = open("myhelsinki_events.txt", "r+")
beolv1 = json.loads(f.read())
f.close()

x1 = beolv1["data"]
hossz1 = len(x1)

gpsVek = np.zeros((hossz1, 3))

for i in range(hossz1):
    gpsVek[i, 0] = x1[i]["location"]["lat"]
    gpsVek[i, 1] = x1[i]["location"]["lon"]

latKoord = 60.17
lonKoord = 24.95
gpsKoord = np.array([latKoord, lonKoord])

for i in range(hossz1):
    gpsVek[i, 2] = np.sum((gpsVek[i, 0:2] - gpsKoord) * (gpsVek[i, 0:2] - gpsKoord))

tagSzotar = beolv1["tags"]
hossz2 = len(tagSzotar)

tagSzotar2 = {}
ind = 0
for i in tagSzotar:
    ert = tagSzotar.get(i)
    tagSzotar2[ert] = ind
    ind += 1

fullMtx1 = np.zeros((hossz1, hossz2))

eventIds = []
for i in range(hossz1):
    eventIds.append(x1[i]["id"])
    for j in x1[i]["tags"]:
        fullMtx1[i, tagSzotar2.get(j["name"])] = 1

corrMtx = np.corrcoef(fullMtx1, rowvar=False)
corrMtx2 = np.nan_to_num(corrMtx)

csere1 = np.zeros((2, 1))
for i in range(hossz2):
    tempvek = np.where(corrMtx2[i, :] > 0.7)
    # print(tempvek[0])
    for j in range(len(tempvek[0])):
        if i != tempvek[0][j]:
            csere1 = np.append(csere1, [[i], [tempvek[0][j]]], axis=1)

csere1 = csere1[:, 1:]
cserehossz = csere1[0, :].size

cserevek = np.ones(hossz2)
for i in range(cserehossz):
    if cserevek[int(csere1[0, i])] == 1:
        cserevek[int(csere1[1, i])] = 0

tagSzotarRovid1 = {}
for i in range(hossz2):
    if cserevek[i] == 1:
        temp = list(tagSzotar.keys())[i]
        temp2 = tagSzotar.get(temp)
        tagSzotarRovid1[temp] = temp2

hosszrovid = len(tagSzotarRovid1)

fullMtx1r = fullMtx1 * cserevek

ember = np.zeros(hossz2)
ember[0] = 1
ember[1] = 0
ember[2] = 1
ember[3] = 0
ember[4] = 1
ember[5] = 0
ember[6] = 1

# emberu = np.zeros(hossz2)
# kerdes_db = 10
# kerdes_idk = []
# kerdes_tagek = []
# for i in range(kerdes_db):
#     randid = np.random.randint(0, hosszrovid)
#     temp = list(tagSzotarRovid1.keys())[randid]
#     kerdes_idk.append(temp)
#     temp2 = tagSzotarRovid1.get(temp)
#     kerdes_tagek.append(temp2)
#     emberu[tagSzotar2.get(temp2)] = 1

# after this we could search the best events to him/her
output_events = 3
# (indexek, tavok) = knn1(ember, fullMtx1r, output_events)
(indexek, tavok) = knn2(ember, fullMtx1r, output_events, gpsVek[:, 2], maxdist=0.005)

# here the indexek store the numerical index of the event, we could read out the event from eventIds
out_event_list = []
for i in range(output_events):
    out_event_list.append(eventIds[int(indexek[i])])

eventsapi = cmyhelsinki.CMyHelsinki()

###########################################xxxxxxxxxxxxxxxxxxx


stopsapi = cstops.CStops()

stations = stopsapi.get_station_locations()

fig = go.Figure()

stops = stopsapi.get_stations_tram()

fig.add_scattermapbox(lat=stops['lat'], lon=stops['lon'], mode="markers",
                      marker=dict(size=8, color="blue"))

fig.add_scattermapbox(lat=sensors['lat'], lon=sensors['lon'], mode="markers",
                      marker=dict(size=12, color="black"))

fig.update_layout(
    mapbox={
        'accesstoken': 'pk.eyJ1Ijoibm9yYmVydDg4IiwiYSI6ImNrMjgyY2Z4ZTF2dnQzYm16OXJmcDk3N3kifQ.BIt4mQU4oNObibeDEC7Yjg',
        'style': "open-street-map", 'zoom': 13, 'center': go.layout.mapbox.Center(lon=24.9471, lat=60.1602)},
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    showlegend=False)

for i in out_event_list:
    event = eventsapi.get_specific_event(i)
    fig.add_scattermapbox(lon=[event['location']['lon']], lat=[event['location']['lat']],
                          mode="markers+text", text="próba", textposition="top center",
                          marker=dict(size=25, color="brown"), name="", hovertext="próba3", hoverinfo="text",
                          customdata=[[event['description']['intro'], event['info_url']]],
                          hovertemplate='<b>%{customdata[0]}</b><br><br>%{customdata[1]}')
for j in out_event_list:
    event = eventsapi.get_specific_event(j)
    print(event['location'])
    coords = ((24.91438, 60.14947), (event['location']['lon'], event['location']['lat']))
    client = openrouteservice.Client(
        key='5b3ce3597851110001cf62486ec15dbb6fa040b1b964169eebc6824d')  # Specify your personal API key
    geometry = client.directions(coords)['routes'][0]['geometry']
    coordis = convert.decode_polyline(geometry)
    print(coordis)
    xlist = []
    ylist = []
    for i in coordis['coordinates']:
        xlist.append(i[0])
        ylist.append(i[1])
    fig.add_scattermapbox(lat=ylist, lon=xlist, mode="lines", marker=dict(size=20, color="red"))

fig.show()
