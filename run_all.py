import re
from argparse import ArgumentParser
from functools import cache, partial
from itertools import combinations, product
from math import prod
from scipy.optimize import linprog
from time import perf_counter


parser = ArgumentParser()
parser.add_argument("-e", "--example", action="store_true")
parser.add_argument("-d", "--days", default="1-25")
args = parser.parse_args()

EXAMPLE = args.example

interval = r"(\d{1,2}|\d{1,2}-\d{1,2})"
if re.match(rf"{interval}(,{interval})*", args.days):
    days = set()
    for part in args.days.split(","):
        interval = tuple(map(int, part.split("-")))
        for n in interval:
            if n == 0 or 25 < n:
                parser.error(f"-d: wrong argument(s): {n}")
        start, stop = interval[0], interval[-1]
        if start != stop and stop < start:
            parser.error(f"-d: wrong argument(s): {start} > {stop}")
        days.update(range(start, stop + 1))
else:
    parser.error("-d: wrong format!")
selected_days = tuple(sorted(days))        


def day_1():
    print("Day 1:")

    file_name = f"2025/input/day_01{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        ROTATIONS = tuple((line[:1], int(line[1:])) for line in file)


    def part_1():
        position, count = 50, 0
        for direction, no in ROTATIONS:
            if direction == "R":
                position = (position + no) % 100
            else:
                position = (position - no) % 100
            if position == 0:
                count += 1
        return count


    print(f"  - part 1:", solution := part_1())
    assert solution == (3 if EXAMPLE else 1102)


    def part_2():
        position, count = 50, 0
        for direction, no in ROTATIONS:
            full, rest = divmod(no, 100)
            count += full
            if rest == 0:
                continue
            if direction == "R":
                position_new = position + rest
                count += position_new >= 100
            else:
                position_new = position - rest
                count += position and position_new <= 0
            position = position_new % 100
        return count


    print(f"  - part 2:", solution := part_2())
    assert solution == (6 if EXAMPLE else 6175)


def day_2():
    print("Day 2:")

    file_name = f"2025/input/day_02{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        ranges = file.read().rstrip()
    RANGES = tuple(tuple(map(int, r.split("-"))) for r in ranges.split(","))


    def part_1():
        pwd = 0
        for start, end in RANGES:
            for n in range(start, end + 1):
                mid, rest = divmod(len(n_str := str(n)), 2)
                if rest == 0 and n_str[:mid] == n_str[mid:]:
                    pwd += n            
        return pwd


    print(f"  - part 1:", solution := part_1())
    assert solution == (1227775554 if EXAMPLE else 30608905813)


    def part_2():
        pwd = 0
        for length in range(2, max(len(str(end)) for _, end in RANGES) + 1):
            invalids = set()
            for n in range(1, length):
                if length % n != 0:
                    continue
                reps = length // n
                for part in range(10 ** (n - 1), 10 ** n):
                    invalids.add(int(str(part) * reps))
            for n in invalids:
                for start, end in RANGES:
                    if start <= n <= end:
                        pwd += n
                        break
        return pwd


    print(f"  - part 2:", solution := part_2())
    assert solution == (4174379265 if EXAMPLE else 31898925685)


def day_3():
    print("Day 3:")

    file_name = f"2025/input/day_03{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        BANKS = tuple(tuple(map(int, line.rstrip())) for line in file)
    LENGTH = len(BANKS[0])


    def solve(num_digits):
        total = 0
        for bank in BANKS:
            joltage, start, stop = 0, 0, LENGTH - num_digits + 1
            for _ in range(num_digits):
                i = max(range(start, stop), key=lambda i: bank[i])
                joltage = 10 * joltage + bank[i]
                start, stop = i + 1, stop + 1
            total += joltage
        return total
 

    print(f"  - part 1:", solution := solve(2))
    assert solution == (357 if EXAMPLE else 17142)
    print(f"  - part 2:", solution := solve(12))
    assert solution == (3121910778619 if EXAMPLE else 169935154100102)


def day_4():
    print("Day 4:")

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


    print(f"  - part 1:", solution := len(removable(ROLLS)))
    assert solution == (13 if EXAMPLE else 1376)


    def part_2():
        rolls = set(ROLLS)
        while True:
            remove = removable(rolls)
            if not remove:
                break
            rolls.difference_update(remove)
        return len(ROLLS) - len(rolls)
 

    print(f"  - part 2:", solution := part_2())
    assert solution == (43 if EXAMPLE else 8587)


def day_5():
    print("Day 5:")

    file_name = "2025/input/day_05" + ("_example" if EXAMPLE else "") + ".txt"
    with open(file_name, "r") as file:
        ranges = []
        for line in file:
            if not (line := line.rstrip()):
                break
            ranges.append(tuple(map(int, line.split("-"))))
        RANGES = tuple(ranges)
        IDS = tuple(map(int, file))

 
    def part_1():
        count = 0
        for n in IDS:
            for left, right in RANGES:
                if left <= n <= right:
                    count += 1
                    break
        return count
 

    print(f"  - part 1:", solution := part_1())
    assert solution == (3 if EXAMPLE else 885)
 

    def part_2():
        ranges, count, start, stop = sorted(RANGES), 0, 0, -1
        for left, right in ranges:
            if left <= stop:
                stop = max(stop, right)
            else:
                count += stop - start + 1
                start, stop = left, right
        return count + stop - start + 1
 

    print(f"  - part 2:", solution := part_2())
    assert solution == (14 if EXAMPLE else 348115621205535)


def day_6():
    print("Day 6:")

    file_name = f"2025/input/day_06{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        lines = file.read().splitlines()
    NUMBERS, OPS = tuple(lines[:-1]), tuple(lines[-1].split())


    def part_1():
        numbers = (tuple(map(int, line.split())) for line in NUMBERS)
        return sum(
            sum(ns) if op == "+" else prod(ns)
            for ns, op in zip(zip(*numbers), OPS)
        )


    print(f"  - part 1:", solution := part_1())
    assert solution == (4277556 if EXAMPLE else 6209956042374)


    def part_2():
        numbers, row = [], []
        for chars in zip(*NUMBERS):
            num = "".join(chars).strip()
            if num:
                row.append(int(num))
            else:
                numbers.append(tuple(row))
                row = []
        numbers.append(tuple(row))
        return sum(
            sum(ns) if op == "+" else prod(ns)
            for ns, op in zip(numbers, OPS)
        )


    print(f"  - part 2:", solution := part_2())
    assert solution == (3263827 if EXAMPLE else 12608160008022)


def day_7():
    print("Day 7:")

    file_name = f"2025/input/day_07{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        MANIFOLD = tuple(file.read().splitlines())


    def part_1():
        splits = 0
        beams = [MANIFOLD[0].index("S")]
        for row in MANIFOLD[1:]:
            beams_new = []
            for b in beams:
                if row[b] == ".":
                    if not beams_new or beams_new[-1] != b:
                        beams_new.append(b)
                else:
                    splits += 1
                    b_new = b - 1
                    if not beams_new or beams_new[-1] != b_new:
                        beams_new.append(b_new)
                    beams_new.append(b + 1)
            beams = beams_new
        return splits


    print(f"  - part 1:", solution := part_1())
    assert solution == (21 if EXAMPLE else 1490)


    def part_2():
        beams = {MANIFOLD[0].index("S"): 1}
        for row in MANIFOLD[1:]:
            beams_new = {}
            for b, count in beams.items():
                if row[b] == ".":
                    beams_new[b] = beams_new.get(b, 0) + count
                else:
                    b_new = b - 1
                    beams_new[b_new] = beams_new.get(b_new, 0) + count
                    beams_new[b + 1] = count
            beams = beams_new
        return sum(beams.values())


    print(f"  - part 2:", solution := part_2())
    assert solution == (40 if EXAMPLE else 3806264447357)


def day_8():
    print("Day 8:")

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
    print(f"  - part 1: {solution_1}")
    assert solution_1 == (40 if EXAMPLE else 69192)
    print(f"  - part 2: {solution_2}")
    assert solution_2 == (25272 if EXAMPLE else 7264308110)


def day_9():
    print("Day 9:")

    file_name = f"2025/input/day_09{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        REDS = tuple(tuple(map(int, line.split(","))) for line in file)


    def area(tile_1, tile_2):
        (r1, c1), (r2, c2) = tile_1, tile_2
        return (abs(r1 - r2) + 1) * (abs(c1 - c2) + 1)


    def part_1():
        return max(area(t1, t2) for t1, t2 in combinations(REDS, r=2))


    print(f"  - part 1:", solution := part_1())
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


    print(f"  - part 2:", solution := part_2())
    assert solution == (24 if EXAMPLE else 1525991432)


def day_10():
    print("Day 10:")

    file_name = f"2025/input/day_10{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        machines = []
        for line in file:
            parts = line.rstrip().split()
            machine = [parts[0].strip("[]")]
            machine.extend(
                tuple(map(int, part[1:-1].split(",")))
                for part in parts[1:]
            )
            machines.append(machine)
    MACHINES = tuple(machines)


    def part_1():
        result = 0
        for machine in MACHINES:
            target = [0 if char == "." else 1 for char in machine[0]]
            buttons = [
                [1 if n in button else 0 for n in range(len(target))]
                for button in machine[1:-1]
            ]
            matrix = [*zip(*buttons)]
            minimum = float("inf")
            for xs in product([0, 1], repeat=len(buttons)):
                num = sum(xs)
                if num >= minimum:
                    continue
                for row, b in zip(matrix, target):
                    if sum(x * r for x, r in zip(xs, row)) % 2 != b:
                        break
                else:
                    minimum = num
            result += minimum
        return result


    print(f"  - part 1:", solution := part_1())
    assert solution == (7 if EXAMPLE else 532)


    def part_2():
        count = 0
        for machine in MACHINES:
            idxs = range(len(machine[0]))
            buttons = [
                [1 if n in button else 0 for n in idxs]
                for button in machine[1:-1]
            ]
            num_variables = len(buttons)
            c = [1] * num_variables
            A = [list(row) for row in zip(*buttons)]
            b = list(machine[-1])
            res = linprog(c, A_eq=A, b_eq=b, integrality=list(c))
            count += res.fun
    
        return int(count)


    print(f"  - part 2:", solution := part_2())
    assert solution == (33 if EXAMPLE else 18387)


def day_11():
    print("Day 11:")

    file_name = f"2025/input/day_11{'_example_1' if EXAMPLE else ''}.txt"
    CONNECTS = {}
    with open(file_name, "r") as file:
        for line in file:
            left, right = line.rstrip().split(": ")
            CONNECTS[left] = tuple(right.split())


    def part_1():
        count = 0
        stack = [["you"]]
        while stack:
            path = stack.pop()
            for node in CONNECTS[path[-1]]:
                if node == "out":
                    count += 1
                elif node not in path:
                    stack.append(path + [node])
        return count


    print(f"  - part 1:", solution := part_1())
    assert solution == (5 if EXAMPLE else 497)

    if EXAMPLE:
        CONNECTS = {}
        with open("2025/input/day_11_example_2.txt", "r") as file:
            for line in file:
                left, right = line.rstrip().split(": ")
                CONNECTS[left] = set(right.split())
        pprint(CONNECTS)


    def part_2():
        graph = {}
        for n0, nodes in CONNECTS.items():
            for n1 in nodes:
                graph.setdefault(n1, set()).add(n0)
    
        @cache
        def count(node):
            if node == "svr":
                return {"none": 1, "fft": 0, "dac": 0, "both": 0}
        
            counts_new = {"none": 0, "fft": 0, "dac": 0, "both": 0}
            for n in graph[node]:
                counts = count(n)
                if node == "fft":
                    counts_new["fft"] += counts["none"]
                    counts_new["both"] += counts["dac"]
                elif node == "dac":
                    counts_new["dac"] += counts["none"]
                    counts_new["both"] += counts["fft"]
                else:
                    for state in "none", "fft", "dac", "both":
                        counts_new[state] += counts[state]
        
            return counts_new
        
        return count("out")["both"]


    print(f"  - part 2:", solution := part_2())
    assert solution == (2 if EXAMPLE else 358564784931864)


days = {
    1: day_1,
    2: day_2,
    3: day_3,
    4: day_4,
    5: day_5,
    6: day_6,
    7: day_7,
    8: day_8,
    9: day_9,
    10: day_10,
    11: day_11
}


if __name__ == "__main__":


    total_ms = 0
    for day in selected_days:
        if day not in days: continue
        func = days[day]
        start = perf_counter()
        func()
        end = perf_counter()
        ms = (end - start) * 1_000
        print(f"  => run time: {ms:.0f} ms\n")
        total_ms += ms
    print(f"\n=> total run time: {total_ms:.0f} ms\n")
