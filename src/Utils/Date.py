import re
from datetime import datetime
from zoneinfo import ZoneInfo


def iso_local_timestamp_to_datetime(timestamp: str) -> datetime:
    """Converts a non-TZ'd timestamp in the ISO 8601 format to a datetime object."""

    # If not matches YYYY-MM-DDTHH:mm:ss
    if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", timestamp):
        raise ValueError(f"Invalid timestamp: {timestamp}")

    year, month, day = timestamp.split("T")[0].split("-")
    hour, minute, second = timestamp.split("T")[1].split(":")

    return datetime(
        int(year),
        int(month),
        int(day),
        int(hour),
        int(minute),
        int(second),
        tzinfo=ZoneInfo("Europe/London"),
    )
