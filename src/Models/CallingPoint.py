from typing import Union


class CallingPoint:
    def __init__(self, json: dict, isServiceCancelled: bool):
        self.locationName: str = json["locationName"]
        self.crs: str = json["crs"]
        self.scheduledTime: str = json["st"]
        self.estimatedTime: str = json["et"]
        self.actualTime: Union[str, None] = json["at"]
        self.isCancelled: bool = json["isCancelled"]

        self.__isServiceCancelled: bool = isServiceCancelled

    def __str__(self) -> str:
        eta = self.estimatedTime

        if eta == "On time":
            eta = self.scheduledTime

        return (
            f"{self.locationName}{f' ({eta})' if not self.__isServiceCancelled else ''}"
        )
