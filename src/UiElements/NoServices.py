from Drawable import Drawable
from PIL import ImageDraw

from assets.CustomPixelFontSmall import SmallFont, SmallFont_Size


class NoServices(Drawable):
    def draw(self, c: ImageDraw.ImageDraw):
        pos = self._pos
        dev = self._device

        lines = [
            "Please listen for announcements",
            "or call National Rail Enquiries",
            "on 03457 48 49 50",
        ]

        sizes = [c.textsize(line, font=SmallFont) for line in lines]

        for i, line in enumerate(lines):
            x = (dev.width - sizes[i][0]) // 2

            c.text(
                (x + pos[0], ((SmallFont_Size + 3) * i) + pos[1]),
                line,
                font=SmallFont,
                fill="white",
            )
