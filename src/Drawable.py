from PIL import ImageDraw
from luma.oled.device import ssd1322


class Drawable:
    def __init__(
        self, canvas: ImageDraw.ImageDraw, device: ssd1322, pos: tuple[int, int]
    ):
        self._canvas: ImageDraw.ImageDraw = canvas
        self._device: ssd1322 = device
        self._pos: tuple[int, int] = pos

    def draw(self):
        pass
