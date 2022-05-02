import timing

from color import Color
from disc import Disc
from move import Move
from solver import Solver
from table import Table

DISC_0 = Disc(
    slots=[
        Color.from_int(0),
        Color.from_int(1),
        Color.from_int(4),
        Color.from_int(5),
        Color.from_int(2),
        Color.from_int(3),
    ]
)
DISC_1 = Disc(
    slots=[
        Color.from_int(0),
        Color.from_int(2),
        Color.from_int(1),
        Color.from_int(3),
        Color.from_int(4),
        Color.from_int(5),
    ]
)
DISC_2 = Disc(
    slots=[
        Color.from_int(0),
        Color.from_int(3),
        Color.from_int(4),
        Color.from_int(2),
        Color.from_int(1),
        Color.from_int(5),
    ]
)
DISC_3 = Disc(
    slots=[
        Color.from_int(0),
        Color.from_int(3),
        Color.from_int(5),
        Color.from_int(4),
        Color.from_int(2),
        Color.from_int(1),
    ]
)
DISC_4 = Disc(
    slots=[
        Color.from_int(0),
        Color.from_int(4),
        Color.from_int(2),
        Color.from_int(3),
        Color.from_int(5),
        Color.from_int(1),
    ]
)
DISC_5 = Disc(
    slots=[
        Color.from_int(0),
        Color.from_int(4),
        Color.from_int(2),
        Color.from_int(5),
        Color.from_int(3),
        Color.from_int(1),
    ]
)
DISC_6 = Disc(
    slots=[
        Color.from_int(0),
        Color.from_int(5),
        Color.from_int(1),
        Color.from_int(2),
        Color.from_int(4),
        Color.from_int(3),
    ]
)

ALL_DISCS = [DISC_0, DISC_1, DISC_2, DISC_3, DISC_4, DISC_5, DISC_6]

if __name__ == "__main__":
    known_solutions = [
        Move(
            center=DISC_4,
            perimeter=[
                DISC_2,
                DISC_0.rotate_clockwise(2),
                DISC_3.rotate_clockwise(4),
                DISC_1.rotate_clockwise(3),
                DISC_6.rotate_clockwise(1),
                DISC_5.rotate_clockwise(5),
            ],
            remaining_discs=[],
        )
    ]
    empty_table = Table()
    solver = Solver(table=empty_table, discs=ALL_DISCS)
    solution = solver.solve()
    if solution:
        print("\n" * 3)
        print(solution.center)
        for disc in solution.perimeter:
            print(disc)
        print(solution.remaining_discs)
