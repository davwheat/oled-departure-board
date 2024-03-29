from .SecondaryService import SecondaryService
from PIL import ImageDraw
from luma.core.device import device

from assets.CustomPixelFontSmall import SmallFont, SmallFont_Size

from AppState import AppState

from Utils.CachedText import cachedBitmapText

from typing import Union

_calling_at_frame_rid: Union[None, str] = None
_calling_at_frame_counter = 0


class PrimaryService(SecondaryService):
    def __init__(self, dev: device, pos: tuple[int, int], ordinal: int):
        super().__init__(dev, pos, ordinal)

    def __draw_details(self, c: ImageDraw.ImageDraw):
        global _calling_at_frame_rid, _calling_at_frame_counter

        assert self._service is not None

        pos = self._pos
        service = self._service
        device = self._device

        text = service.callingPointsText()
        desc_text = "Calling at: "

        stops_width, _, stops_bitmap = cachedBitmapText(text, SmallFont)
        desc_width, desc_height, desc_bitmap = cachedBitmapText(desc_text, SmallFont)

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
            (scroller_x_pos, pos[1] + SmallFont_Size + 3), stops_bitmap, fill="white"
        )

        c.rectangle(
            (
                pos[0],
                pos[1] + SmallFont_Size + 3,
                pos[0] + self.ordinal_width + self.time_width - 1,
                pos[1] + (SmallFont_Size + 3) + desc_height,
            ),
            fill="black",
        )

        c.bitmap((pos[0], pos[1] + SmallFont_Size + 3), desc_bitmap, fill="white")

    def draw(self, c: ImageDraw.ImageDraw, position_offset: tuple[int, int] = (0, 0)):
        super().draw(c, position_offset)
        self.__draw_details(c)
