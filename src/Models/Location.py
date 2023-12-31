from typing import Union


class Location:
    def __init__(self, json: dict):
        self.locationName: str = json["locationName"]
        self.crs: str = json["crs"]
        self.via: Union[str, None] = json["via"]

    def __str__(self) -> str:
        if self.via is None:
            return self.locationName

        return f"{self.locationName} {self.via}"

    def to_snippets(self) -> list[str]:
        if self.via is None:
            return [self.locationName]

        return [self.locationName, self.via]
