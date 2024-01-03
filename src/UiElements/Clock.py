from Drawable import Drawable
from PIL import ImageDraw

from zoneinfo import ZoneInfo
from datetime import datetime

from assets.CustomPixelFontClock import ClockFont
from Utils.CachedText import cachedBitmapText


class Clock(Drawable):
    def draw(self, c: ImageDraw.ImageDraw):
        pos = self._pos

        # Get time HH:mm:ss
        time = datetime.now(ZoneInfo("Europe/London"))

        hour = "%02d" % time.hour
        min = "%02d" % time.minute
        secs = "%02d" % time.second

        widthPerChar = 10
        colonWidth = 5

        _, height, h1 = cachedBitmapText(hour[0], ClockFont)
        _, _, h2 = cachedBitmapText(hour[1], ClockFont)
        _, _, m1 = cachedBitmapText(min[0], ClockFont)
        _, _, m2 = cachedBitmapText(min[1], ClockFont)
        _, _, s1 = cachedBitmapText(secs[0], ClockFont)
        _, _, s2 = cachedBitmapText(secs[1], ClockFont)
        _, _, colon = cachedBitmapText(":", ClockFont)

        pos_x_start: int = pos[0] - ((6 * widthPerChar + 2 * colonWidth) // 2)
        pos_y: int = pos[1] - height

        # Hour chars
        c.bitmap((pos_x_start, pos_y), h1, fill="white")
        c.bitmap((pos_x_start + widthPerChar, pos_y), h2, fill="white")

        # Min chars
        c.bitmap((pos_x_start + 2 * widthPerChar + colonWidth, pos_y), m1, fill="white")
        c.bitmap((pos_x_start + 3 * widthPerChar + colonWidth, pos_y), m2, fill="white")

        # Sec chars
        c.bitmap(
            (pos_x_start + 4 * widthPerChar + 2 * colonWidth, pos_y), s1, fill="white"
        )
        c.bitmap(
            (pos_x_start + 5 * widthPerChar + 2 * colonWidth, pos_y), s2, fill="white"
        )

        # Colons
        c.bitmap((pos_x_start + widthPerChar * 2, pos_y), colon, fill="white")
        c.bitmap(
            (pos_x_start + widthPerChar * 4 + colonWidth, pos_y), colon, fill="white"
        )
