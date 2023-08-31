from dataclasses import dataclass
from typing import Union

from Models.Train import Train


@dataclass
class AppState:
    # Trains to display
    trains: Union[list[Train], None] = None

    fps: int = 60
