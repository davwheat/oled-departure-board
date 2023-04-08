from Models.Location import Location

from typing import Union


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

    def destinationText(self) -> list[str]:
        return [str(destination) for destination in self.destination]

    def originText(self) -> list[str]:
        return [str(origin) for origin in self.origin]
