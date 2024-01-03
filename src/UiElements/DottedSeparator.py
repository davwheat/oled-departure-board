from Drawable import Drawable
from PIL import ImageDraw
from luma.core.device import device


class DottedSeparator(Drawable):
    def __init__(
        self,
        dev: device,
        pos: tuple[int, int],
        width: int,
    ):
        super().__init__(dev, pos)
        self._width = width

    def draw(self, c: ImageDraw.ImageDraw):
        pos = self._pos
        width = self._width

        for i in range(pos[0], pos[0] + width, 2):
            c.line(
                (
                    pos[0] + i,
                    pos[1],
                    pos[0] + i,
                    pos[1],
                ),
                fill="white",
                width=1,
            )
