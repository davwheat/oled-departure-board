from Models.Train import Train

from typing import Union

import requests

__DEBUG_FILE: Union[None, str] = "./Api/exampleQuery.json"
# __DEBUG_FILE: Union[None, str] = None


def __generateUrl(stationCrs: str, servicesCount: int = 3) -> str:
    """Generates a URL to a Huxley 2 compatible API endpoint."""
    return f"https://national-rail-api.davwheat.dev/departures/{stationCrs}/{servicesCount}?expand=true"


def fetchServicesFromStation(stationCrs: str) -> list[Train]:
    """Fetches a list of trains from a station."""

    if __DEBUG_FILE is not None:
        import json

        with open(__DEBUG_FILE, "r") as f:
            data = json.load(f)
    else:
        url = __generateUrl(stationCrs)

        # Fetch JSON from server
        try:
            resp = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Network error: failed to fetch train data. ({e})")
            return []

        if not resp.ok:
            print(
                f"API Error: failed to fetch train data. (Status code: {resp.status_code})"
            )
            return []

        data = resp.json()

    if data["trainServices"] is None:
        return []

    # Parse JSON into a list of trains
    trains = [Train(x) for x in data["trainServices"]]

    return trains
