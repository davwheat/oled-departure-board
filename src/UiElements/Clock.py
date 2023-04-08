from Drawable import Drawable

from zoneinfo import ZoneInfo
from datetime import datetime

from assets.CustomPixelFont import CustomPixelFont


class Clock(Drawable):
    def draw(self):
        c = self._canvas
        pos = self._pos

        # Get time HH:mm:ss
        time = datetime.now(ZoneInfo("Europe/London"))

        hour = time.strftime("%H")
        min = time.strftime("%M")
        secs = time.strftime("%S")

        widthPerChar = 12
        colonWidth = 5

        myFont = CustomPixelFont
        _, height = c.textsize(hour, font=myFont)

        pos_x_start: int = pos[0] - ((6 * widthPerChar + 2 * colonWidth) // 2)
        pos_y: int = pos[1] - height

        # Hour char 1
        c.text((pos_x_start, pos_y), hour[0], font=myFont, fill="white")
        # Hour char 2
        c.text((pos_x_start + widthPerChar, pos_y), hour[1], font=myFont, fill="white")

        # Min char 1
        c.text(
            (pos_x_start + 2 * widthPerChar + colonWidth, pos_y),
            min[0],
            font=myFont,
            fill="white",
        )
        # Min char 2
        c.text(
            (pos_x_start + 3 * widthPerChar + colonWidth, pos_y),
            min[1],
            font=myFont,
            fill="white",
        )

        # Sec char 1
        c.text(
            (pos_x_start + 4 * widthPerChar + 2 * colonWidth, pos_y),
            secs[0],
            font=myFont,
            fill="white",
        )
        # Sec char 2
        c.text(
            (pos_x_start + 5 * widthPerChar + 2 * colonWidth, pos_y),
            secs[1],
            font=myFont,
            fill="white",
        )

        # Colon 1
        c.text(
            (pos_x_start + widthPerChar * 2 + 1, pos_y),
            "¦",
            font=myFont,
            fill="white",
        )
        # Colon 2
        c.text(
            (pos_x_start + widthPerChar * 4 + colonWidth + 1, pos_y),
            "¦",
            font=myFont,
            fill="white",
        )
