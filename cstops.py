import numpy as np
import requests
import json
import pandas as pd

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def get_distance(x, y, a, b):
    return np.linalg.norm(np.array([x, y]) - np.array([a, b]))


class CStops:
    _transport = RequestsHTTPTransport(
        url='https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql',
        use_json=True,
    )

    client = Client(
        transport=_transport,
        fetch_schema_from_transport=True,
    )

    # {
    #     stations
    # {
    #     gtfsId
    # name
    # lat
    # lon
    # stops
    # {
    #     gtfsId
    # name
    # code
    # platformCode
    # }
    # }
    # }

    def get_stations(self):
        query = gql("""
            {
                stations {
                    gtfsId
                    name
                    lat
                    lon
                }
            }
            """)
        return json.dumps(self.client.execute(query), indent=4, sort_keys=True)

    def get_nearest_station(self, x, y):
        stops = json.loads(self.get_stations())
        absmin = ""
        minstation = ""
        for i in stops['stations']:
            mind = get_distance(i['lat'], i['lon'], x, y)
            if absmin == "" or mind < absmin:
                absmin = mind
                minstation = i
        return json.dumps(minstation, indent=4, sort_keys=True)

    def get_station_locations(self):
        data = {'name': [], 'lat': [], 'lon': []}
        df = pd.DataFrame(data)
        stops = json.loads(self.get_stations())
        for i in stops['stations']:
            df = df.append({'name': i['name'], 'lat': i['lat'], 'lon': i['lon']}, ignore_index=True)
        return df

    def get_stations_tram(self):
        query = gql("""
            {
                routes(name: "7", transportModes: TRAM) {
                    shortName
                    longName
                    stops {
                        name
                        lat
                        lon
                        patterns {
                            directionId
                        }
                    }
                }
            }
            """)
        data = {'name': [], 'lat': [], 'lon': []}
        df = pd.DataFrame(data)
        stops = self.client.execute(query)

        for i in stops['routes'][0]['stops']:
            df = df.append({'name': i['name'], 'lat': i['lat'], 'lon': i['lon']}, ignore_index=True)
        return df
        # return json.dumps(stops['routes'][0], indent=4, sort_keys=True)
