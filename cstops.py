import requests
import json

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class CStops:

    _transport = RequestsHTTPTransport(
        url='https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql',
        use_json=True,
    )

    client = Client(
        transport=_transport,
        fetch_schema_from_transport=True,
    )

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
        print(json.dumps(self.client.execute(query), indent=4, sort_keys=True))

