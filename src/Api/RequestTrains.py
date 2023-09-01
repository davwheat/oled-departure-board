from Models.Train import Train
from Utils.Log import debug, error

import requests

from typing import Union

__DEBUG_FILE: Union[None, str] = None
# __DEBUG_FILE: Union[None, str] = "./Api/exampleQuery.3.json"


def __generateUrl(stationCrs: str, servicesCount: int = 8) -> str:
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
            error(f"Network error: failed to fetch train data. ({e})")
            return []

        if not resp.ok:
            error(
                f"API Error: failed to fetch train data. (Status code: {resp.status_code})"
            )
            return []

        data = resp.json()

    if data["trainServices"] is None:
        return []

    # Parse JSON into a list of trains
    trains: list[Train] = []

    for service in data["trainServices"]:
        train = Train(service)

        # Get time diff in minutes
        time_diff = train.estimatedDepartingInMinutes()

        # Ignore trains that have already departed
        if time_diff is not None and time_diff < -1:
            continue

        trains.append(train)

    return trains
