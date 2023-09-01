from Drawable import Drawable
from PIL import ImageDraw

from assets.CustomPixelFontSmall import SmallFont, SmallFont_Size

from Utils.CachedText import cachedBitmapText


class NoServices(Drawable):
    def draw(self, c: ImageDraw.ImageDraw):
        pos = self._pos
        dev = self._device

        lines = [
            "Please listen for announcements",
            "or call National Rail Enquiries",
            "on 03457 48 49 50",
        ]

        parsed_lines = [cachedBitmapText(line, SmallFont) for line in lines]

        for i, line in enumerate(parsed_lines):
            x = (dev.width - line[0]) // 2

            c.bitmap(
                (x + pos[0], ((SmallFont_Size + 3) * i) + pos[1]),
                line[2],
                fill="white",
            )
