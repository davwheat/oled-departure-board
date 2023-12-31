from Utils.Date import iso_local_timestamp_to_datetime

from typing import Union

from datetime import datetime


class CallingPoint:
    def __init__(self, json: dict, isServiceCancelled: bool):
        self.locationName: str = json["locationName"]
        self.crs: str = json["crs"]
        self.isCancelled: bool = json["isCancelled"]

        self.schedDepTime: Union[datetime, None] = (
            iso_local_timestamp_to_datetime(json["std"])
            if json["stdSpecified"]
            else None
        )
        self.actualDepTime: Union[str, None] = (
            iso_local_timestamp_to_datetime(json["atd"])
            if json["atdSpecified"]
            else None
        )
        self.estDepTime: Union[str, None] = (
            iso_local_timestamp_to_datetime(json["etd"])
            if json["etdSpecified"]
            else None
        )

        self.schedArrTime: Union[str, None] = (
            iso_local_timestamp_to_datetime(json["sta"])
            if json["staSpecified"]
            else None
        )
        self.actualArrTime: Union[str, None] = (
            iso_local_timestamp_to_datetime(json["ata"])
            if json["ataSpecified"]
            else None
        )
        self.estArrTime: Union[str, None] = (
            iso_local_timestamp_to_datetime(json["eta"])
            if json["etaSpecified"]
            else None
        )

        self.__isServiceCancelled: bool = isServiceCancelled

        self.most_accurate_arr_time: datetime = self.__most_accurate_arr_time()
        self.most_accurate_dep_time: datetime = self.__most_accurate_dep_time()

    def __most_accurate_arr_time(self) -> datetime:
        """
        Returns the most accurate arrival time.

        This is the actual arrival time if it exists, otherwise the estimated arrival time, otherwise the scheduled arrival time.
        """

        if self.actualArrTime is not None:
            return self.actualArrTime
        elif self.estArrTime is not None:
            return self.estArrTime
        else:
            return self.schedArrTime

    def __most_accurate_dep_time(self) -> datetime:
        """
        Returns the most accurate departure time.

        This is the actual departure time if it exists, otherwise the estimated departure time, otherwise the scheduled departure time.
        """

        if self.actualDepTime is not None:
            return self.actualDepTime
        elif self.estDepTime is not None:
            return self.estDepTime
        else:
            return self.schedDepTime

    def __str__(self) -> str:
        eta_text = self.most_accurate_arr_time.strftime("%H:%M")

        return f"{self.locationName}{f' ({eta_text})' if not self.__isServiceCancelled or self.isCancelled else ''}"
