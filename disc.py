from typing import List

from color import Color


class Disc:
    def __init__(self, slots: List[Color]):
        """Constructor for Disc.

        If this is a perimeter disc:
        - slot[0] always faces the center disc.
        - slot[-1] always faces the disc which is at the next clockwise position.
        - slot[1] always faces the disc which is at the next anti-clockwise position.

        If this is a center disc:
        - slot[i] faces the slot[0] of the disc in perimeter[i].
        """
        assert len(slots) == 6
        self.slots = slots
        self.rotation = 0

    def rotate_clockwise(self, times):
        """Rotate the disc changing the color
        in each slot (0<-1, 1<-2, ..., 4<-5, 5<-0).
        """
        assert times > 0
        if self.rotation + times > 5:
            raise Exception("I won't turn anymore")
        for time in range(times):
            saved_slot = self.slots[0]
            for idx in range(5):
                self.slots[idx] = self.slots[idx + 1]
            self.slots[5] = saved_slot
            self.rotation += 1

    def __repr__(self):
        return f"{self.__class__.__name__}{self.slots},rotation:{self.rotation}"

    def reset(self):
        if self.rotation == 0:
            return
        for time in range(6 - self.rotation):
            saved_slot = self.slots[0]
            for idx in range(1, 5):
                self.slots[idx] = self.slots[idx + 1]
            self.slots[5] = saved_slot
        self.rotation = 0
