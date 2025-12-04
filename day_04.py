# --------------------------------------------------------------------------- #
#    Day 4                                                                    #
# --------------------------------------------------------------------------- #
from argparse import ArgumentParser
from pprint import pprint


# --------------------------------------------------------------------------- #
#    Preparation                                                              #
# --------------------------------------------------------------------------- #
print("Day 4")

parser = ArgumentParser()
parser.add_argument("-e", "--example", action="store_true")
EXAMPLE = parser.parse_args().example


def print_grid(rolls, removes=None):
    if removes is None:
        removes = set()
    string = "\n".join(
        "".join(
            "x" if (r, c) in removes else "@" if (r, c) in rolls else "."
            for c in range(COLS)
        )
        for r in range(ROWS)
    )
    print(string, end="\n\n")


# --------------------------------------------------------------------------- #
#    Reading input                                                            #
# --------------------------------------------------------------------------- #

file_name = f"2025/input/day_04{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    rolls = file.read().splitlines()
ROWS, COLS = len(rolls), len(rolls[0])
ROLLS = {
    (r, c)
    for r, row in enumerate(rolls)
    for c, char in enumerate(row)
    if char == "@"
}

if EXAMPLE:
    print(f"# of rows: {ROWS}")
    print(f"# of columns: {COLS}")
    print("rolls:\n")
    print_grid(ROLLS)

# --------------------------------------------------------------------------- #
#    Helpers                                                                  #
# --------------------------------------------------------------------------- #

DRC = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
 

def removable(rolls):
    removable = []
    for r, c in rolls:
        count = 0
        for dr, dc in DRC:
            count += (r + dr, c + dc) in rolls
            if count > 3:
                break
        if count < 4:
            removable.append((r, c))
    return removable


# --------------------------------------------------------------------------- #
#    Part 1                                                                   #
# --------------------------------------------------------------------------- #
print("Part 1: ", end="")

print(solution := len(removable(ROLLS)))
assert solution == (13 if EXAMPLE else 1376)

# --------------------------------------------------------------------------- #
#    Part 2                                                                   #
# --------------------------------------------------------------------------- #
print("Part 2: ", end="")


def part_2(show=False):
    rolls = set(ROLLS)
    while True:
        remove = removable(rolls)
        if not remove:
            break
        rolls.difference_update(remove)
        if show:
            print_grid(rolls, remove) 
    return len(ROLLS) - len(rolls)
 

if EXAMPLE:
    print("\n")
    solution = part_2(show=True)
    print(f"solution: {solution}")
else:
    print(solution := part_2())
assert solution == (43 if EXAMPLE else 8587)
