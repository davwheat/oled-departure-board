from Models.Location import Location
from Models.CallingPoint import CallingPoint

from Utils.String import pluralise

from typing import Union

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

arrived_trains: dict[str, float] = {}


class Train:
    def __init__(self, json: dict):
        self.origin: list[Location] = [Location(origin) for origin in json["origin"]]
        self.destination: list[Location] = [
            Location(destination) for destination in json["destination"]
        ]

        self.schedDepTime: str = json["std"]
        self.estDepTime: str = json["etd"]

        self.schedArrTime: Union[str, None] = json["sta"]
        self.estArrTime: Union[str, None] = json["eta"]

        self.isCancelled: bool = json["isCancelled"]

        self.platform: str = json["platform"]

        self.operator: str = json["operator"]
        self.operatorCode: str = json["operatorCode"]

        self.length: Union[int, None] = json["length"]

        self.delayReason: Union[str, None] = json["delayReason"]
        self.cancelReason: Union[str, None] = json["cancelReason"]

        self.guid: str = json["serviceIdGuid"]

        self.callingPoints = [
            CallingPoint(x, self.isCancelled)
            for x in json["subsequentCallingPoints"][0]["callingPoint"]
        ]

    def is_arriving(self) -> bool:
        """Returns whether the train is arriving at the station."""

        global arrived_trains

        # Remove trains that have been marked as arrived for more than 1hr
        arrived_trains = {
            guid: timestamp
            for guid, timestamp in arrived_trains.items()
            if timestamp > datetime.now().timestamp()
        }

        eta_mins = self.estimatedDepartingInMinutes()

        if eta_mins is not None and eta_mins < 1:
            # set to arrived, remove after 1hr
            arrived_trains[self.guid] = datetime.now().timestamp() + 3600.0

        return self.guid in arrived_trains

    def destinationText(self) -> list[str]:
        return [str(destination) for destination in self.destination]

    def originText(self) -> list[str]:
        return [str(origin) for origin in self.origin]

    def estimatedDepartingInMinutes(self) -> Union[float, None]:
        """Returns the estimated time in minutes until the train departs."""

        sched_dep_time = self.schedDepTime
        est_dept_time = self.estDepTime

        if self.isCancelled or est_dept_time == "On time":
            est_dept_time = sched_dep_time
        elif est_dept_time == "Delayed":
            return None

        # If not matches HH:mm
        if not re.match(r"^\d{2}:\d{2}$", est_dept_time):
            return None

        est_hour, est_min = est_dept_time.split(":")

        now = datetime.now(ZoneInfo("Europe/London"))
        est_time = datetime(
            now.year,
            now.month,
            now.day,
            int(est_hour),
            int(est_min),
            tzinfo=ZoneInfo("Europe/London"),
        )

        # Handle midnight and day rollover
        if now.hour < 12:
            # If before midday
            if est_time.hour < 9:
                est_time -= timedelta(days=1)
        else:
            # If after midday
            if est_time.hour < 9:
                est_time += timedelta(days=1)

        # Get time diff in minutes
        time_diff = (est_time - now).total_seconds() / 60

        return time_diff

    def callingPointsText(self) -> str:
        """Returns the calling points as a string."""

        if len(self.callingPoints) == 1:
            return str(self.callingPoints[0]) + " only."

        return (
            pluralise([str(callingPoint) for callingPoint in self.callingPoints]) + "."
        )
