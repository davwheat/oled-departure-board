from Drawable import Drawable
from PIL import ImageDraw

from assets.CustomPixelFontSmall import SmallFont, SmallFont_Size

from Models.Train import Train
from AppState import AppState

from Utils.CachedText import cachedBitmapText

from typing import Union

_cancelled_frame_counter = 0
_cancelled_frame_counter_max = AppState.fps * 2
_cancelled_frame_counter_iterated = False


_destination_frame_counter = 0
_destination_frame_counter_max = 0

_calling_at_frame_guid: Union[None, str] = None
_calling_at_frame_counter = 0
_calling_at_frame_counter_max = 0


class PrimaryService(Drawable):
    ordinal_width = 26

    # nums are 7 px wide,
    # colon is 5 px wide
    # plus small gap for spacing
    time_width = (7 * 4) + (5) + (4)

    est_time_spacing = 4

    def __init__(self, device, pos, service: Train):
        super().__init__(device, pos)
        self._service: Train = service
        self.service_guid = service.guid

    def __del__(self):
        global _cancelled_frame_counter_iterated
        _cancelled_frame_counter_iterated = False

    def __increment_cancelled_frame_counter(self):
        global _cancelled_frame_counter, _cancelled_frame_counter_iterated, _cancelled_frame_counter_max

        _cancelled_frame_counter_iterated = True
        _cancelled_frame_counter += 1

        # 2 secs
        if _cancelled_frame_counter > _cancelled_frame_counter_max:
            _cancelled_frame_counter = 0

    def __get_cancelled_text_opacity(self) -> int:
        global _cancelled_frame_counter, _cancelled_frame_counter_max

        half_point = _cancelled_frame_counter_max // 2

        if _cancelled_frame_counter < half_point:
            return int(_cancelled_frame_counter / half_point * 255)
        else:
            return int(
                (1 - ((_cancelled_frame_counter - half_point) / half_point)) * 255
            )

    def __draw_ordinal(self, c: ImageDraw.ImageDraw, root_pos: tuple[int, int]):
        _, _, text = cachedBitmapText("1st", SmallFont)
        c.bitmap((root_pos[0], root_pos[1]), text, fill="white")

    def __draw_scheduled_time(self, c: ImageDraw.ImageDraw, root_pos: tuple[int, int]):
        _, _, text = cachedBitmapText(self._service.schedDepTime, SmallFont)
        c.bitmap((root_pos[0], root_pos[1]), text, fill="white")

    def __get_destination_snippets(self) -> list[str]:
        all_snippets: list[list[str]] = [
            dest.to_snippets() for dest in self._service.destination
        ]

        snippet_group_count = len(all_snippets)
        for i, snippet_group in enumerate(all_snippets):
            # Handle adding "and" between destinations where multiple are present
            snippet_count = len(snippet_group)

            if i < snippet_group_count - 1:
                snippet_group[snippet_count - 1] += " and"
            elif snippet_group_count > 1:
                snippet_group[0] = "and " + snippet_group[0]

        flattened_snippets: list[str] = []

        for snippet_group in all_snippets:
            for snippet in snippet_group:
                flattened_snippets.append(snippet)

        return flattened_snippets

    def __draw_destination(self, c: ImageDraw.ImageDraw, root_pos: tuple[int, int]):
        global _destination_frame_counter_max, _destination_frame_counter

        snippets = self.__get_destination_snippets()
        snippet_count = len(snippets)

        # 5 secs per snippet
        length_per_snippet = AppState.fps * 5

        expected_dest_frame_counter_max = snippet_count * length_per_snippet

        if _destination_frame_counter_max != expected_dest_frame_counter_max:
            _destination_frame_counter = 0
            _destination_frame_counter_max = expected_dest_frame_counter_max
        else:
            _destination_frame_counter += 1
            if _destination_frame_counter >= _destination_frame_counter_max:
                _destination_frame_counter = 0

        snippet_num_to_show = _destination_frame_counter // length_per_snippet

        _, _, text = cachedBitmapText(snippets[snippet_num_to_show], SmallFont)
        c.bitmap((root_pos[0], root_pos[1]), text, fill="white")

    def __get_est_time_text(self) -> str:
        estDepTimeText: str = self._service.estDepTime

        if self._service.isCancelled:
            estDepTimeText = "Cancelled"
        elif self._service.is_arriving():
            estDepTimeText = f"Arrived"
        elif estDepTimeText not in ["On time", "Delayed"]:
            estDepTimeText = f"Expt {estDepTimeText}"

        return estDepTimeText

    def __get_est_time_width(self, c: ImageDraw.ImageDraw) -> float:
        # width of est dep time
        estDepTextWidth, _, _ = cachedBitmapText(self.__get_est_time_text(), SmallFont)

        return estDepTextWidth

    def __draw_est_time(self, c: ImageDraw.ImageDraw):
        self.__increment_cancelled_frame_counter()

        pos = self._pos

        estDepTimeText: str = self.__get_est_time_text()
        estDepTextX = self._device.width - self.__get_est_time_width(c)

        # Backup in case of overflow from destination text
        c.rectangle(
            (
                estDepTextX - self.est_time_spacing,
                pos[1],
                self._device.width,
                pos[1] + 16,
            ),
            fill="black",
        )

        color = "white"

        if self._service.isCancelled:
            color = (
                self.__get_cancelled_text_opacity(),
                self.__get_cancelled_text_opacity(),
                self.__get_cancelled_text_opacity(),
            )

        # "On time"
        _, _, text = cachedBitmapText(estDepTimeText, SmallFont)
        c.bitmap((estDepTextX, pos[1]), text, fill=color)

    def __draw_details(self, c: ImageDraw.ImageDraw):
        global _calling_at_frame_guid, _calling_at_frame_counter

        pos = self._pos
        service = self._service
        device = self._device

        text = service.callingPointsText()
        desc_text = "Calling at: " if not service.isCancelled else "Was calling at: "

        stops_width, _, stops_text = cachedBitmapText(text, SmallFont)
        desc_width, _, desc_text = cachedBitmapText(desc_text, SmallFont)

        # Reset scroller if service has changed
        if _calling_at_frame_guid != service.guid:
            _calling_at_frame_guid = service.guid
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
                pos[0] + desc_width,
                pos[1] + (SmallFont_Size + 3) * 2,
            ),
            fill="black",
        )

        c.bitmap((pos[0], pos[1] + SmallFont_Size + 3), desc_text, fill="white")

    def draw(self, c: ImageDraw.ImageDraw):
        self.__draw_ordinal(c, (self._pos[0], self._pos[1]))
        self.__draw_scheduled_time(c, (self._pos[0] + self.ordinal_width, self._pos[1]))
        self.__draw_destination(
            c, (self._pos[0] + self.ordinal_width + self.time_width, self._pos[1])
        )
        self.__draw_est_time(c)
        self.__draw_details(c)
