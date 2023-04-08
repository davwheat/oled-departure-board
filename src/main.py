import os
from threading import Thread
from timed_count import timed_count

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

from AppState import AppState
from Api.RequestTrains import fetchServicesFromStation

from typing import Union


fps: int = 60
frameperiod: float = 1.0 / fps
now: float = time()
nextframe: float = now + frameperiod
device: Union[ssd1322, None] = None

data_refresh_rate = 120


def periodic():
    for _ in timed_count(60):
        update_data()


def update_data():
    print("Updating data...")

    services = fetchServicesFromStation("ECR")

    AppState.trains = services

    print(f"Updated data. {len(services)} services found.")


def main():
    global nextframe, frameperiod, now, device

    thread = Thread(target=periodic)
    thread.start()

    serial = spi(device=0, port=0)

    device = ssd1322(serial)

    while True:
        now = time()

        while now < nextframe:
            sleep(nextframe - now)
            now = time()

        nextframe += frameperiod

        draw_frame()


def draw_frame():
    global device

    if device is None:
        print("Device not initialized")
        exit(1)

    with canvas(device) as c:
        clock = Clock(c, device, (device.width // 2, device.height))
        clock.draw()

        if AppState.trains is None:
            return

        if len(AppState.trains) == 0:
            return



if __name__ == "__main__":
    main()
