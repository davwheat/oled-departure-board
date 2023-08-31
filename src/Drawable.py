from PIL import ImageDraw
from luma.oled.device import ssd1322


class Drawable:
    def __init__(self, device: ssd1322, pos: tuple[int, int]):
        self._device: ssd1322 = device
        self._pos: tuple[int, int] = pos

    def draw(self, canvas: ImageDraw.ImageDraw):
        pass
