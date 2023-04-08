from typing import Union


class Location:
    def __init__(self, json: dict):
        self.locationName: str = json["locationName"]
        self.crs: str = json["crs"]
        self.via: Union[str, None] = json["via"]
        # self.futureChangeTo: Union[str, None] = json["futureChangeTo"]
        self.assocIsCancelled: bool = json["assocIsCancelled"]

    def __str__(self) -> str:
        if self.via is None:
            return self.locationName

        return f"{self.locationName} {self.via}"
