import os
from threading import Thread
from timed_count import timed_count

from AppState import AppState

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
from UiElements.NoServices import NoServices

from AppState import AppState
from Api.RequestTrains import fetchServicesFromStation
from Utils.Log import debug, error

from typing import Union


_frameperiod: float = 1.0 / AppState.fps
_now: float = time()
_nextframe: float = _now + _frameperiod
_device: Union[ssd1322, None] = None

_data_refresh_rate = 60


def periodic():
    for _ in timed_count(_data_refresh_rate):
        update_data()


def update_data():
    debug("Updating data...")

    services = fetchServicesFromStation("WVF")

    AppState.trains = services

    debug(f"Updated data. {len(services)} services found.")


def main():
    global _nextframe, _frameperiod, _now, _device

    thread = Thread(target=periodic)
    thread.start()

    serial = spi(device=0, port=0)

    _device = ssd1322(serial)

    while True:
        _now = time()

        while _now < _nextframe:
            sleep(_nextframe - _now)
            _now = time()

        _nextframe += _frameperiod

        draw_frame()


def draw_frame():
    global _device

    if _device is None:
        error("Device not initialized")
        exit(1)

    clock = Clock(_device, (_device.width // 2, _device.height))
    primary_service: Union[None, PrimaryService] = None

    with canvas(_device) as c:
        clock.draw(c)

        if AppState.trains is None or len(AppState.trains) == 0:
            no_services = NoServices(_device, (0, 0))
            no_services.draw(c)
            return

        if (
            primary_service is None
            or primary_service.service_guid != AppState.trains[0].guid
        ):
            primary_service = PrimaryService(_device, (0, -1), AppState.trains[0])

        primary_service.draw(c)


if __name__ == "__main__":
    main()
