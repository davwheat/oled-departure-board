import json
import os

__location_name_overrides: dict[str, str] = json.load(
    open(os.path.join(os.path.dirname(__file__), "./location_name_overrides.json"), "r")
)


def get_location_name_with_override(crs: str, provided_name: str) -> str:
    if crs in __location_name_overrides:
        return __location_name_overrides[crs]
    return provided_name
