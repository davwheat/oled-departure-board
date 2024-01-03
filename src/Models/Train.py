from Models.Location import Location
from Models.CallingPoint import CallingPoint

from Utils.String import pluralise
from Utils.Date import iso_local_timestamp_to_datetime

from typing import Union

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


class Train:
    def __init__(self, currentCrs: str, json: dict):
        self.origin: list[Location] = [Location(origin) for origin in json["origin"]]
        self.destination: list[Location] = [
            Location(destination) for destination in json["destination"]
        ]

        self.schedDepTime: datetime | None = (
            iso_local_timestamp_to_datetime(json["std"])
            if json["stdSpecified"]
            else None
        )
        self.actualDepTime: datetime | None = (
            iso_local_timestamp_to_datetime(json["atd"])
            if json["atdSpecified"]
            else None
        )
        self.estDepTime: datetime | None = (
            iso_local_timestamp_to_datetime(json["etd"])
            if json["etdSpecified"]
            else None
        )

        self.schedArrTime: datetime | None = (
            iso_local_timestamp_to_datetime(json["sta"])
            if json["staSpecified"]
            else None
        )
        self.actualArrTime: datetime | None = (
            iso_local_timestamp_to_datetime(json["ata"])
            if json["ataSpecified"]
            else None
        )
        self.estArrTime: datetime | None = (
            iso_local_timestamp_to_datetime(json["eta"])
            if json["etaSpecified"]
            else None
        )

        self.isPassengerService: bool = json["isPassengerService"]

        self.isCancelled: bool = json["isCancelled"]

        self.platform: str = json["platform"]

        self.operator: str = json["operator"]
        self.operatorCode: str = json["operatorCode"]

        self.length: int | None = json["length"]

        self.delayReason: str | None = json["delayReason"]
        self.cancelReason: str | None = json["cancelReason"]

        self.rid: str = f"{currentCrs}_{json['rid']}"

        self.callingPoints = [
            CallingPoint(x, self.isCancelled)
            for x in json["subsequentLocations"]
            if not x["isPass"] and not x["isOperational"]
        ]

        self.most_accurate_arr_time: datetime = self.__most_accurate_arr_time()
        self.most_accurate_dep_time: datetime = self.__most_accurate_dep_time()

    def has_arrived(self) -> bool:
        """Returns whether the train has arrived at the station."""

        return self.actualArrTime is not None

    def has_departed(self) -> bool:
        """Returns whether the train gas departed the station."""

        return self.actualDepTime is not None

    def destinationText(self) -> list[str]:
        return [str(destination) for destination in self.destination]

    def originText(self) -> list[str]:
        return [str(origin) for origin in self.origin]

    def callingPointsText(self) -> str:
        """Returns the calling points as a string."""

        points = [
            x for x in self.callingPoints if self.isCancelled or not x.isCancelled
        ]

        if len(points) == 1:
            return str(points[0]) + " only."

        return pluralise([str(p) for p in points]) + "."

    def scheduled_departure_text(self) -> str:
        """Returns the scheduled departure time as a string."""

        if self.schedDepTime is None:
            return "XX:XX"

        return "%02d:%02d" % (self.schedDepTime.hour, self.schedDepTime.minute)

    def estimated_departure_text(self) -> str:
        """Returns the estimated departure time as a string."""

        if self.actualDepTime is not None:
            return "%02d:%02d" % (self.actualDepTime.hour, self.actualDepTime.minute)
        if self.estDepTime is not None and self.schedDepTime is not None:
            edt = "%02d:%02d" % (self.estDepTime.hour, self.estDepTime.minute)
            sdt = "%02d:%02d" % (self.schedDepTime.hour, self.schedDepTime.minute)

            if edt != sdt:
                return f"Expt {edt}"

            return "On time"
        else:
            return "Delayed"

    def __most_accurate_arr_time(self) -> datetime:
        """
        Returns the most accurate arrival time.

        This is the actual arrival time if it exists, otherwise the estimated arrival time, otherwise the scheduled arrival time.
        """

        if self.actualArrTime is not None:
            return self.actualArrTime
        elif self.estArrTime is not None:
            return self.estArrTime
        elif self.schedArrTime is not None:
            return self.schedArrTime
        else:
            return datetime.fromtimestamp(0)

    def __most_accurate_dep_time(self) -> datetime:
        """
        Returns the most accurate departure time.

        This is the actual departure time if it exists, otherwise the estimated departure time, otherwise the scheduled departure time.
        """

        if self.actualDepTime is not None:
            return self.actualDepTime
        elif self.estDepTime is not None:
            return self.estDepTime
        elif self.schedDepTime is not None:
            return self.schedDepTime
        else:
            return datetime.fromtimestamp(0)
