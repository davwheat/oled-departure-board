from typing import Union


class CallingPoint:
    def __init__(self, json: dict):
        self.locationName: str = json["locationName"]
        self.crs: str = json["crs"]
        self.scheduledTime: str = json["st"]
        self.estimatedTime: str = json["et"]
        self.actualTime: Union[str, None] = json["at"]

    def __str__(self) -> str:
        eta = self.estimatedTime

        if eta == "On time":
            eta = self.scheduledTime

        return f"{self.locationName} ({eta})"
