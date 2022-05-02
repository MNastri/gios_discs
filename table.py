from typing import List

from disc import Disc


class Table:
    """A table has 7 places to store discs, one in the center and six in the perimeter.
    The slots in the discs align in such a way that:
    - Table.center.slots[i] aligns with Table.perimeter[i].slots[0], i in
        {0, 1, ..., 5}.
    - Table.perimeter[j].slots[1] aligns with Table.perimeter[j-1].slots[-1],
        j in {0, 1, ..., 5}.
    """

    def __init__(self, center: Disc = None, perimeter: List[Disc] = None):
        """Constructor for Table."""
        self.center = center
        if perimeter is None:
            self.perimeter = [None] * 6
        else:
            assert (
                len(perimeter) == 6
            ), "all places should be defined. Empty places should be None"
            self.perimeter = perimeter

    @property
    def places(self):
        return [self.center, *self.perimeter]

    @property
    def empty_places_perimeter(self):
        return [idx for idx, place in enumerate(self.perimeter) if place is None]

    @property
    def index_of_first_empty_place_perimeter(self):
        if len(self.empty_places_perimeter) == 0:
            return 0
        return self.empty_places_perimeter[0]

    @property
    def number_of_empty_places(self):
        return self.places.count(None)

    @property
    def is_valid(self):
        if self.number_of_empty_places >= 5:
            return True
        if not self._check_center_placement():
            return False
        if not self._check_perimeter_placement():
            return False
        return True

    def _check_center_placement(self):
        """Checks if the center disc has matching colors with the perimeter discs."""
        if self.center is not None:
            for ii in range(6):
                if self.perimeter[ii] is None:
                    continue
                center_slot = self.center.slots[ii]
                perimeter_slot = self.perimeter[ii].slots[0]
                if center_slot.color != perimeter_slot.color:
                    return False
        return True

    def _check_perimeter_placement(self):
        """Checks if the perimeter discs have their slots with matching colors."""
        for ii in range(6):
            curr_disc = self.perimeter[ii]
            if curr_disc is None:
                continue
            curr_disc_next_slot = curr_disc.slots[1]
            curr_disc_prev_slot = curr_disc.slots[-1]
            next_disc = self.perimeter[(ii + 1) % 6]
            if next_disc is not None:
                next_disc_slot = next_disc.slots[1]
                if curr_disc_prev_slot.color != next_disc_slot.color:
                    return False
            prev_disc = self.perimeter[ii - 1]
            if prev_disc is not None:
                prev_disc_slot = prev_disc.slots[-1]
                if curr_disc_next_slot.color != prev_disc_slot.color:
                    return False
        return True

    @property
    def is_solved(self):
        return self.number_of_empty_places == 0 and self.is_valid

    def place_at_perimeter(self, idx, disc):
        self.perimeter[idx] = disc

    def remove_at_perimeter(self, idx):
        self.perimeter[idx] = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.places})"
