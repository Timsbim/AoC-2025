from itertools import combinations


print("Day 9")
EXAMPLE = False


file_name = f"2025/input/day_09{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    REDS = tuple(tuple(map(int, line.split(","))) for line in file)


def area(tile_1, tile_2):
    (r1, c1), (r2, c2) = tile_1, tile_2
    return (abs(r1 - r2) + 1) * (abs(c1 - c2) + 1)


def part_1():
    return max(area(t1, t2) for t1, t2 in combinations(REDS, r=2))


print("Part 1:", solution := part_1())
assert solution == (50 if EXAMPLE else 4748769124)


def key(combo): return area(*combo)


def state(border, c_min, r, c):
    state = "out"
    for c in range(c_min + 1, c + 1):
        match state:
            case "out":
                if (r, c) in border:
                    state = "border"
                    direction = "up" if (r - 1, c) in border else "down"
            case "border":
                if (r, c) not in border:
                    if (r - 1, c) in border:
                        state = "out" if direction == "up" else "in"
                    else:
                        state = "in" if direction == "up" else "out"
            case _:
                if (r, c) in border:
                    state = "border"
                    direction = "up" if (r - 1, c) in border else "down"
    return "in" if state in ("in", "border") else "out"


def part_2():
    edges = tuple(zip(REDS, [*REDS[1:], REDS[0]]))
    border = set()
    for (r1, c1), (r2, c2) in edges:
        if r1 == r2:
            c1, c2 = (c2, c1) if c2 < c1 else (c1, c2)
            border |= {(r1, c) for c in range(c1, c2 + 1)}
        else:
            r1, r2 = (r2, r1) if r2 < r1 else (r1, r2)
            border |= {(r, c1) for r in range(r1, r2 + 1)}

    c_min = min(c for _, c in REDS) - 1
    
    combos = combinations(REDS, r=2)
    for (r1, c1), (r2, c2) in sorted(combos, key=key, reverse=True):
        r1, r2 = (r2, r1) if r2 < r1 else (r1, r2)
        c1, c2 = (c2, c1) if c2 < c1 else (c1, c2)
        if r1 == r2:
            continue
        elif c1 == c2:
            continue
        else:
            if state(border, c_min, r1 + 1, c1 + 1) != "in":
                continue
        for (rr1, cc1), (rr2, cc2) in edges:
            if rr1 == rr2:
                cc1, cc2 = (cc2, cc1) if cc2 < cc1 else (cc1, cc2)
                if r1 < rr1 < r2 and (cc1 < c2 and c1 < cc2):
                    break
            else:
                rr1, rr2 = (rr2, rr1) if rr2 < rr1 else (rr1, rr2)
                if c1 < cc1 < c2 and (rr1 < r2 and r1 < rr2):
                    break
        else:
            return area((r1, c1), (r2, c2))


print("Part 2:", solution := part_2())
assert solution == (24 if EXAMPLE else 1525991432)
