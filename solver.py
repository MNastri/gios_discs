from copy import deepcopy
from typing import List

from disc import Disc
from move import Move
from table import Table

DEBUG = True


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

    def __init__(
        self,
        table: Table,
        discs: List[Disc],
        known_solutions=None,
        depth_first=True,
        move_tracker=None,
    ):
        """Constructor for Solver."""
        assert (
            table.number_of_empty_places - len(discs) == 0
        ), "why are you doing this!?"
        self.table = table
        self.discs = discs
        if known_solutions is None:
            self.known_solutions = []
        else:
            self.known_solutions = known_solutions
        self._depth_first = depth_first
        if move_tracker is None:
            self._move_tracker = ""
        else:
            self._move_tracker = move_tracker
        self._possible_moves = []
        self.counter = -1

    def __repr__(self):
        return f"{self.__class__.__name__}({self.table},remaining_discs:{self.discs})"

    def solve(self) -> Move:
        if self._depth_first:
            return self.solve_depth_first()
        else:
            return self.solve_breadth_first()

    def solve_depth_first(self):
        if self.table.is_solved:
            return self.solution
        if self.not_enough_discs:
            return False
        if self.table.center is None:
            for disc in self.discs:
                discs = [deepcopy(dd) for dd in self.discs if dd != disc]
                next_move = self.create_move_from_copies(
                    disc, self.table.perimeter, discs
                )
                if DEBUG:
                    self.debug_next_move(next_move)
                solution = self.run_next_solver(next_move)
                if DEBUG and solution and solution in self.known_solutions:
                    self.debug_known_solution_found(solution)
                    return False
                elif solution and solution in self.known_solutions:
                    return False
                elif solution:
                    return solution
        else:
            index_first_empty = self.table.index_of_first_empty_place_perimeter
            for disc in self.discs:
                next_move = self.test_disc_at_perimeter_index(disc, index_first_empty)
                if next_move and DEBUG:
                    self.debug_next_move(next_move)
                if next_move:
                    solution = self.run_next_solver(next_move)
                    if DEBUG and solution and solution in self.known_solutions:
                        self.debug_known_solution_found(solution)
                        return False
                    elif solution and solution in self.known_solutions:
                        return False
                    elif solution:
                        return solution

    def solve_breadth_first(self):
        if self.table.is_solved:
            return self.solution
        # TODO code maybe unecessary,check if this is even possible to happen
        if self.not_enough_discs:
            return False
        self.find_possible_moves()
        while self.possible_moves:
            next_move = self.pop_move()
            solution = self.run_next_solver(next_move)
            if solution:
                return solution
        return False

    @property
    def solution(self):
        solution = self.create_move_from_copies(
            self.table.center, self.table.perimeter, self.discs
        )
        return solution  # TODO DEAL WITH DEBUG AND KNOWN SOLUTION

    @property
    def possible_moves(self):
        return self._possible_moves

    @property
    def not_enough_discs(self):
        return len(self.discs) < self.table.number_of_empty_places

    @property
    def move_tracker(self):
        return f"{self._move_tracker}{self.counter}"

    def create_move_from_copies(self, center, perimeter, discs):
        dc = deepcopy
        next_move = Move(dc(center), dc(perimeter), discs)
        return next_move

    def pop_move(self) -> Move:
        return self._possible_moves.pop(0)

    def append_move(self, move_obj: Move):
        self._possible_moves.append(move_obj)

    def find_possible_moves(self):
        if self.table.center is None:
            self.find_possible_center_moves()
        else:
            possible_moves = self.find_possible_perimeter_moves()
            if possible_moves:
                self._possible_moves.extend(possible_moves)
        if DEBUG:
            self.debug_possible_moves()

    def find_possible_center_moves(self):
        assert len(self.discs) == 7
        for disc in self.discs:
            discs = [deepcopy(dd) for dd in self.discs if dd != disc]
            new_move = self.create_move_from_copies(disc, self.table.perimeter, discs)
            self.append_move(new_move)

    def find_possible_perimeter_moves(self):
        index_first_empty = self.table.index_of_first_empty_place_perimeter
        possible_moves = []
        for disc in self.discs:
            new_move = self.test_disc_at_perimeter_index(disc, index_first_empty)
            if new_move:
                possible_moves += (new_move,)
        return possible_moves

    def run_next_solver(self, next_move):
        next_table = Table(next_move.center, next_move.perimeter)
        move_tracker = deepcopy(self.move_tracker)
        next_solver = Solver(
            next_table,
            next_move.remaining_discs,
            self.known_solutions,
            self._depth_first,
            move_tracker,
        )
        solution = next_solver.solve()
        return solution

    def test_disc_at_perimeter_index(self, disc, idx):
        new_disc = deepcopy(disc)
        discs = [deepcopy(dd) for dd in self.discs if dd != disc]
        # TODO instead of checking one by one, find the distance between the desired
        #  color (the color in slots[0] for example) and the present color,
        #  then rotate that many times to pair the wanted color with the desired slot.
        for _ in range(6):
            self.table.place_at_perimeter(idx, new_disc)
            if self.table.is_valid:  # TODO INVERT ORDER OF THIS IF
                new_move = self.create_move_from_copies(
                    self.table.center, self.table.perimeter, discs
                )
                self.table.remove_at_perimeter(idx)
                return new_move
            else:
                self.table.remove_at_perimeter(idx)
                if new_disc.rotation == 5:
                    break
                new_disc.rotate_clockwise(1)

    def debug_table(self):
        print()
        print(self.table)

    def debug_next_move(self, next_move):
        self.counter += 1
        print(f"Move {self.move_tracker:<7}", end=" = ")
        print(f"T({[next_move.center, *next_move.perimeter]})")
        # print(f"{next_move.remaining_discs}")

    def debug_known_solution_found(self, solution):
        print("=" * 20)
        print("SOLUTION FOUND, BUT ALREADY KNOWN")
        print(solution)
        print("=" * 20)

    def debug_possible_moves(self):
        for idx, possible_move in enumerate(self._possible_moves):
            print(
                f"{idx} of {len(self._possible_moves) - 1}", "\n", possible_move.center
            )
            print(f"{possible_move.perimeter}")
            print(f"{possible_move.remaining_discs}")
