from .SecondaryService import SecondaryService
from PIL import ImageDraw
from luma.oled.device import ssd1322

from assets.CustomPixelFontSmall import SmallFont, SmallFont_Size

from Models.Train import Train
from AppState import AppState

from Utils.CachedText import cachedBitmapText

from typing import Union

_calling_at_frame_rid: Union[None, str] = None
_calling_at_frame_counter = 0
_calling_at_frame_counter_max = 0


class PrimaryService(SecondaryService):
    def __init__(
        self, device: ssd1322, pos: tuple[int, int], service: Train, ordinal: int
    ):
        super().__init__(device, pos, service, ordinal)

    def __draw_details(self, c: ImageDraw.ImageDraw):
        global _calling_at_frame_rid, _calling_at_frame_counter

        pos = self._pos
        service = self._service
        device = self._device

        text = service.callingPointsText()
        desc_text = "Calling at: "

        stops_width, _, stops_text = cachedBitmapText(text, SmallFont)
        desc_width, _, desc_text = cachedBitmapText(desc_text, SmallFont)

        # Reset scroller if service has changed
        if _calling_at_frame_rid != service.rid:
            _calling_at_frame_rid = service.rid
            _calling_at_frame_counter = 0
        else:
            _calling_at_frame_counter += 1

        # Reset position if fully scrolled with 2s delay
        if (
            _calling_at_frame_counter
            > stops_width + (device.width - desc_width) + AppState.fps * 2
        ):
            _calling_at_frame_counter = 0

        scroller_x_pos = device.width - (_calling_at_frame_counter)

        c.bitmap(
            (scroller_x_pos, pos[1] + SmallFont_Size + 3), stops_text, fill="white"
        )

        c.rectangle(
            (
                pos[0],
                pos[1] + SmallFont_Size + 3,
                pos[0] + self.ordinal_width + self.time_width - 1,
                pos[1] + (SmallFont_Size + 3) * 2,
            ),
            fill="black",
        )

        c.bitmap((pos[0], pos[1] + SmallFont_Size + 3), desc_text, fill="white")

    def draw(self, c: ImageDraw.ImageDraw):
        super().draw(c)
        self.__draw_details(c)
