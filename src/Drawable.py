from PIL import ImageDraw
from luma.core.device import device


class Drawable:
    def __init__(self, dev: device, pos: tuple[int, int]):
        self._device: device = dev
        self._pos: tuple[int, int] = pos

    def draw(self, canvas: ImageDraw.ImageDraw):
        pass
