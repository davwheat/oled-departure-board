from typing import Union

from Data.Data import get_location_name_with_override


class Location:
    def __init__(self, json: dict):
        self.crs: str = json["crs"]
        self.locationName: str = get_location_name_with_override(
            self.crs, json["locationName"]
        )
        self.via: Union[str, None] = json["via"]

    def __str__(self) -> str:
        if self.via is None:
            return self.locationName

        return f"{self.locationName} {self.via}"

    def to_snippets(self) -> list[str]:
        if self.via is None:
            return [self.locationName]

        return [self.locationName, self.via]
