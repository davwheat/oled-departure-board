import os
from threading import Thread
from typing import cast
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
    parser.add_argument(
        "--emulate",
        action="store_true",
        help="Use emulated display window",
    )
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
from luma.core.device import device

from UiElements.Clock import Clock
from UiElements.PrimaryService import PrimaryService
from UiElements.SecondaryService import SecondaryService
from UiElements.NoServices import NoServices

from AppState import AppState
from Api.RequestTrains import fetchServicesFromStation
from Utils.Log import debug


_frameperiod: float = 1.0 / AppState.fps
_now: float = time()
_nextframe: float = _now + _frameperiod
_device: device | None = None

_data_refresh_rate = 20


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
        draw_loop(bool(args.emulate))
    except Exception as ex:
        traceback.print_exception(ex)


def draw_loop(isEmulated: bool):
    global _nextframe, _frameperiod, _now, _device

    hour_last_cleared_text_cache = int(time()) // 3600

    if isEmulated:
        from luma.emulator.device import pygame

        _device = pygame(width=256, height=64, mode="1", transform="identity", scale=2)
    else:
        serial = spi(device=0, port=0, bus_speed_hz=16_000_000)
        _device = ssd1322(serial, framebuffer="diff_to_previous")

    clock = Clock(_device, (_device.width // 2, _device.height))

    drawables: list[Drawable] = [clock]
    services: list[SecondaryService] = [
        PrimaryService(_device, (0, -1), 1),
        SecondaryService(_device, (0, 32), 2),
    ]

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

        draw_frame(_device, drawables, services)


def draw_frame(
    device: device,
    persistent_drawables: list[Drawable],
    services: list[SecondaryService],
):
    with canvas(device) as c:
        for d in persistent_drawables:
            d.draw(c)

        service_count = 0 if AppState.trains is None else len(AppState.trains)

        if AppState.trains is None or service_count == 0:
            no_services = NoServices(device, (0, 0))
            no_services.draw(c)
            return

        for i, s in enumerate(services):
            if service_count >= i + 1:
                s.set_service(AppState.trains[i])
                s.draw(c)
            else:
                break


if __name__ == "__main__":
    main()
