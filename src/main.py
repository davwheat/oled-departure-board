import os
from threading import Thread
from timed_count import timed_count
import traceback

from AppState import AppState

import argparse
from Drawable import Drawable

from Utils.CachedText import clearBitmapCache


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Display a live departure board for a given station.",
    )
    parser.add_argument("crs_code", metavar="CRS", type=str, nargs=1, help="CRS code")
    return parser


# Reset working directory to file's location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

### Main code ###

from time import time, sleep

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322

from UiElements.Clock import Clock
from UiElements.PrimaryService import PrimaryService
from UiElements.SecondaryService import SecondaryService
from UiElements.NoServices import NoServices

from AppState import AppState
from Api.RequestTrains import fetchServicesFromStation
from Utils.Log import debug, error

from typing import Union


_frameperiod: float = 1.0 / AppState.fps
_now: float = time()
_nextframe: float = _now + _frameperiod
_device: ssd1322 | None = None

_data_refresh_rate = 60


def periodic(crs: str):
    for _ in timed_count(_data_refresh_rate):
        update_data(crs)


def update_data(crs: str):
    debug("Updating data...")

    services = fetchServicesFromStation(crs)

    AppState.trains = services

    debug(f"Updated data. {len(services)} services found.")


def main():
    parser = init_argparse()
    args = parser.parse_args()

    thread = Thread(target=periodic, args=(args.crs_code[0],))
    thread.daemon = True
    thread.start()

    try:
        draw_loop()
    except Exception as ex:
        traceback.print_exception(ex)


def draw_loop():
    global _nextframe, _frameperiod, _now, _device

    hour_last_cleared_text_cache = int(time()) // 3600

    serial = spi(device=0, port=0, bus_speed_hz=10_000_000)

    _device = ssd1322(serial)

    clock = Clock(_device, (_device.width // 2, _device.height))

    drawables: list[Drawable] = [clock]

    frame = 0

    while True:
        _now = time()

        frame = (frame + 1) % AppState.fps

        if frame == 0:
            now_hour = int(time()) // 3600

            if now_hour > hour_last_cleared_text_cache:
                hour_last_cleared_text_cache = now_hour
                debug("Clearing bitmap text cache...")
                clearBitmapCache()

        while _now < _nextframe:
            sleep(_nextframe - _now)
            _now = time()

        _nextframe += _frameperiod

        draw_frame(_device, drawables)


def draw_frame(device: ssd1322, persistent_drawables: list[Drawable]):
    primary_service: Union[None, PrimaryService] = None
    secondary_service: Union[None, SecondaryService] = None

    with canvas(device) as c:
        for d in persistent_drawables:
            d.draw(c)

        if AppState.trains is None or len(AppState.trains) == 0:
            no_services = NoServices(device, (0, 0))
            no_services.draw(c)
            return

        if (
            primary_service is None
            or primary_service.service_rid != AppState.trains[0].rid
        ):
            primary_service = PrimaryService(device, (0, -1), AppState.trains[0], 1)

        if (
            len(AppState.trains) >= 2
            and secondary_service is None
            or len(AppState.trains) < 2
            and secondary_service is not None
            or secondary_service is not None
            and secondary_service.service_rid != AppState.trains[1].rid
        ):
            if len(AppState.trains) < 2:
                secondary_service = None
            else:
                secondary_service = SecondaryService(
                    device, (0, 32), AppState.trains[1], 2
                )

        primary_service.draw(c)

        if secondary_service is not None:
            secondary_service.draw(c)


if __name__ == "__main__":
    main()
