from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322

from time import time, sleep

from UiElements.Clock import Clock

from typing import Union


fps = 60
frameperiod = 1.0 / fps
now = time()
nextframe = now + frameperiod
device: Union[ssd1322, None] = None


def main():
    global nextframe, frameperiod, now, device

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
        clock2 = Clock(c, device, (device.width // 2, device.height - 16))
        clock3 = Clock(c, device, (device.width // 2, device.height - 32))
        clock4 = Clock(c, device, (device.width // 2, device.height - 48))

        clock.draw()
        clock2.draw()
        clock3.draw()
        clock4.draw()


if __name__ == "__main__":
    main()
