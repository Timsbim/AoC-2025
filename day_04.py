print("Day 4")
EXAMPLE = False


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


print("Part 1:", solution := len(removable(ROLLS)))
assert solution == (13 if EXAMPLE else 1376)


def part_2():
    rolls = set(ROLLS)
    while True:
        remove = removable(rolls)
        if not remove:
            break
        rolls.difference_update(remove)
    return len(ROLLS) - len(rolls)
 

print("Part 2:", solution := part_2())
assert solution == (43 if EXAMPLE else 8587)
