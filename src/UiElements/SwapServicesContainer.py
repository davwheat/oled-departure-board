from Drawable import Drawable
from .SecondaryService import SecondaryService
from PIL import ImageDraw
from luma.core.device import device

from assets.CustomPixelFontSmall import SmallFont_Size

from AppState import AppState


class SwapServicesContainer(Drawable):
    _frames_per_service = AppState.fps * 4
    _service_height = SmallFont_Size + 3
    _frame_counter = 0
    _slide_animation_frames = SmallFont_Size

    def __init__(
        self,
        device: device,
        pos: tuple[int, int],
        service_drawables: list[SecondaryService],
    ):
        super().__init__(device, pos)

        self._service_drawables = service_drawables

    def set_service_drawables(self, service_drawables: list[SecondaryService]):
        self._service_drawables = service_drawables

    def draw(self, c: ImageDraw.ImageDraw):
        count = len(self._service_drawables)

        counter_max = count * self._frames_per_service
        if self._frame_counter >= counter_max:
            self._frame_counter = 0

        visible_index = self._frame_counter // self._frames_per_service
        currently_visible = self._service_drawables[visible_index]
        next_visible = self._service_drawables[
            0 if visible_index + 1 >= count else visible_index + 1
        ]

        progress = self._frame_counter % self._frames_per_service
        slide_up_progress = (
            max(0, progress - (self._frames_per_service - self._slide_animation_frames))
            / self._slide_animation_frames
        )

        currently_visible.set_pos(
            (self._pos[0], self._pos[1] - int(slide_up_progress * self._service_height))
        )
        next_visible.set_pos(
            (
                self._pos[0],
                self._pos[1] - int((slide_up_progress - 1) * self._service_height),
            )
        )

        currently_visible.draw(c)
        next_visible.draw(c)

        # Draw rectangles around off-screen services
        c.rectangle(
            (
                self._pos[0],
                self._pos[1] - int(slide_up_progress * self._service_height),
                self._pos[0] + self._device.width,
                self._pos[1],
            ),
            fill="black",
        )

        c.rectangle(
            (
                self._pos[0],
                self._pos[1] + self._service_height,
                self._pos[0] + self._device.width,
                self._pos[1]
                + self._service_height
                - int((slide_up_progress - 1) * self._service_height),
            ),
            fill="black",
        )

        self._frame_counter += 1
