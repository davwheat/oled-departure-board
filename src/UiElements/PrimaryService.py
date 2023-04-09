from Drawable import Drawable

from assets.CustomPixelFontSmall import TestFont

from Models.Train import Train
from AppState import AppState

__frame_counter = 0


class PrimaryService(Drawable):
    def __init__(self, canvas, device, pos, service: Train):
        super().__init__(canvas, device, pos)
        self._service: Train = service

    def draw(self):
        c = self._canvas
        pos = self._pos

        myFont = TestFont

        ordinal_width = 24

        c.text(
            (pos[0], pos[1]),
            "1st",
            font=myFont,
            fill="white",
        )

        # nums are 7 px wide,
        # colon is 5 px wide
        # plus small gap for spacing
        time_width = (7 * 4) + (5) + (5)

        c.text(
            (pos[0] + ordinal_width, pos[1]),
            self._service.schedDepTime,
            font=myFont,
            fill="white",
        )

        c.text(
            (pos[0] + ordinal_width + time_width, pos[1]),
            " and ".join(self._service.destinationText()),
            font=myFont,
            fill="white",
        )

        # width of est dep time
        estDepTextWidth, _ = c.textsize(
            self._service.estDepTime,
            font=myFont,
        )
        estDepTextX = self._device.width - estDepTextWidth
        estDepLeftSpacing = 4

        # Backup in case of overflow from destination text
        c.rectangle(
            (estDepTextX - estDepLeftSpacing, pos[1], self._device.width, pos[1] + 16),
            fill="black",
        )

        # "On time"
        c.text(
            (estDepTextX, pos[1]),
            self._service.estDepTime,
            font=myFont,
            fill="white",
        )
