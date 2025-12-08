from itertools import combinations
from math import prod


print("Day 8")
EXAMPLE = False


file_name = f"2025/input/day_08{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    BOXES = tuple(
        tuple(map(int, line.rstrip().split(",")))
        for line in file
    )


def dist(combo):
    (x1, y1, z1), (x2, y2, z2) = combo
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2


def solve():
    num, num_boxes = 10 if EXAMPLE else 1_000, len(BOXES)
    solution_1 = None
    circuits, connects = [], sorted(combinations(BOXES, r=2), key=dist)
    for n, (box_1, box_2) in enumerate(connects, start=1):
        circuits_new, connect = [], {box_1, box_2}
        for circuit in circuits:
            if box_1 in circuit or box_2 in circuit:
                connect.update(circuit)
            else:
                circuits_new.append(circuit)
        if len(connect) == num_boxes:
            if solution_1 is None:
                solution_1 = num_boxes
            return solution_1, box_1[0] * box_2[0]
        circuits_new.append(connect)
        circuits = circuits_new
        if n == num:
            tops = sorted([*map(len, circuits)], reverse=True)
            solution_1 = prod(tops[:3])


solution_1, solution_2 = solve()
print(f"Part 1: {solution_1}")
assert solution_1 == (40 if EXAMPLE else 69192)
print(f"Part 2: {solution_2}")
assert solution_2 == (25272 if EXAMPLE else 7264308110)
