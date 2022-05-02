from typing import (
    List,
    NamedTuple,
)

from disc import Disc


class Move(NamedTuple):
    center: Disc = None
    perimeter: List[Disc] = [None] * 6
    remaining_discs: List[Disc] = [None]
