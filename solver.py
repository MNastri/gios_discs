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

    def __init__(self, table: Table, discs: List[Disc], known_solutions=[]):
        """Constructor for Solver."""
        assert (
            table.number_of_empty_places - len(discs) == 0
        ), "why are you doing this!?"
        print(table)
        self.table = table
        self.discs = discs
        self.known_solutions = known_solutions
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
        # TODO instead of checking one by one, find the distance between the desired
        #  color (the color in slots[0] for example) and the present color,
        #  then rotate that many times to pair the wanted color with the desired slot.
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
            center = deepcopy(self.table.center)
            perimeter = deepcopy(self.table.perimeter)
            remaining_discs = deepcopy(self.discs)
            solution = Move(
                center=center,
                perimeter=perimeter,
                remaining_discs=remaining_discs,
            )
            if solution in self.known_solutions:
                print("=" * 20 + "\nSOLUTION FOUND, BUT ALREADY KNOWN\n" + "=" * 20)
                return False
            return solution
        # TODO code maybe unecessary,check if this is even possible
        if len(self.discs) < self.table.number_of_empty_places:
            return False
        while self.posssible_moves:
            next_move = self.pop_move()
            next_table = Table(center=next_move.center, perimeter=next_move.perimeter)
            next_solver = Solver(
                table=next_table,
                discs=next_move.remaining_discs,
                known_solutions=self.known_solutions,
            )
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
