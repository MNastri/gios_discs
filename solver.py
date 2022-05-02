from copy import deepcopy
from typing import List

from disc import Disc
from move import Move
from table import Table


class Solver:
    """Receives a table with discs (center and perimeter) and the leftover
    discs, then calculates what are the possible moves and applies one of them (
    the first it finds).
    Sends the new table and leftover discs to another Solver to get the solution
     by recursion.
    If the center disc has not been placed, only branches through the options
    where the center disc is placed, i.e. the solver does not try to solve by
    placing a perimeter disc first.
    The discs attribute contains the remaining unplaced discs.
    """

    def __init__(self, table: Table, discs: List[Disc]):
        """Constructor for Solver."""
        assert (
            table.number_of_empty_places - len(discs) == 0
        ), "why are you doing this!?"
        print(table)
        self.table = table
        self.discs = discs
        self._possible_moves = []
        self.find_possible_moves()

    def find_possible_moves(self):
        if self.table.center is None:
            self._find_possible_center_moves()
        else:
            self._find_possible_perimeter_moves()

    def _find_possible_center_moves(self):
        assert len(self.discs) == 7
        for disc in self.discs:
            new_disc = deepcopy(disc)
            new_perimeter = deepcopy(self.table.perimeter)
            remaining_discs = [deepcopy(dd) for dd in self.discs if dd != disc]
            new_move = Move(
                center=new_disc,
                perimeter=new_perimeter,
                remaining_discs=remaining_discs,
            )
            self.append_move(new_move)

    def _find_possible_perimeter_moves(self):
        index_first_empty = self.table.index_of_first_empty_place_perimeter
        for disc in self.discs:
            self._test_disc_at_perimeter_index(disc, index_first_empty)

    def _test_disc_at_perimeter_index(self, disc, idx):
        new_disc = deepcopy(disc)
        remaining_discs = [deepcopy(dd) for dd in self.discs if dd != disc]
        for _ in range(6):
            self.table.place_at_perimeter(idx, new_disc)
            if self.table.is_valid:
                center = deepcopy(self.table.center)
                perimeter = deepcopy(self.table.perimeter)
                new_move = Move(
                    center=center,
                    perimeter=perimeter,
                    remaining_discs=remaining_discs,
                )
                self.append_move(new_move)
                self.table.remove_at_perimeter(idx)
                break
            else:
                self.table.remove_at_perimeter(idx)
                if new_disc.rotation == 5:
                    break
                new_disc.rotate_clockwise(1)

    def solve(self) -> Move:
        if self.table.is_solved:
            solution = Move(
                center=self.table.center,
                perimeter=self.table.perimeter,
                remaining_discs=self.discs,
            )
            return solution
        if len(self.discs) < self.table.number_of_empty_places:
            return False
        while self.posssible_moves:
            next_move = self.pop_move()
            next_table = Table(center=next_move.center, perimeter=next_move.perimeter)
            next_solver = Solver(table=next_table, discs=next_move.remaining_discs)
            solution = next_solver.solve()
            if isinstance(solution, Move):
                return solution
        return False

    @property
    def posssible_moves(self):
        return self._possible_moves

    def pop_move(self) -> Move:
        return self._possible_moves.pop(0)

    def append_move(self, move_obj: Move):
        self._possible_moves.append(move_obj)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.table},remaining_discs:{self.discs})"
