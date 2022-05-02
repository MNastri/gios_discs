import timing

from color import Color
from disc import Disc
from move import Move
from solver import Solver
from table import Table

DISCS = {
    0: Disc.from_str("014523"),
    1: Disc.from_str("021345"),
    2: Disc.from_str("034215"),
    3: Disc.from_str("035421"),
    4: Disc.from_str("042351"),
    5: Disc.from_str("042531"),
    6: Disc.from_str("051243"),
}
ALL_DISCS = [DISCS[0], DISCS[1], DISCS[2], DISCS[3], DISCS[4], DISCS[5], DISCS[6]]


def setup_known_solutions():
    discs = [4, 2, 0, 3, 1, 6, 5]
    rotations = [0, 0, 2, 4, 3, 1, 5]
    known_solutions = []
    for disc, rotation in zip(discs, rotations):
        if rotation > 0:
            known_solutions += (DISCS[disc].rotate_clockwise(rotation),)
        else:
            known_solutions += (DISCS[disc],)
    return known_solutions


if __name__ == "__main__":
    known_solutions = setup_known_solutions()
    empty_table = Table()
    solver = Solver(table=empty_table, discs=ALL_DISCS, known_solutions=known_solutions)
    solution = solver.solve()

    if known_solutions:
        for known_solution in known_solutions:
            print(known_solution.center)
            for disc in known_solution.perimeter:
                print(disc)
            print(known_solution.remaining_discs)

    if solution:
        print("\n" * 2)
        print(solution.center)
        for disc in solution.perimeter:
            print(disc)
        print(solution.remaining_discs)
