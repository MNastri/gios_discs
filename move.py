from typing import (
    List,
    NamedTuple,
)

from disc import Disc


class Move(NamedTuple):
    center: Disc = None
    perimeter: List[Disc] = [None] * 6
    remaining_discs: List[Disc] = [None]

    def __eq__(self, other):
        if (
            self.center == other.center
            and self.perimeter == other.perimeter
            and self.remaining_discs == other.remaining_discs
        ):
            return True
        return False
