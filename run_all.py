import re
from argparse import ArgumentParser
from math import prod
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
            for beam in beams:
                if row[beam] == ".":
                    if not beams_new or beams_new[-1] != beam:
                        beams_new.append(beam)
                else:
                    splits += 1
                    beam_new = beam - 1
                    if not beams_new or beams_new[-1] != beam_new:
                        beams_new.append(beam_new)
                    beams_new.append(beam + 1)
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


days = {
    1: day_1,
    2: day_2,
    3: day_3,
    4: day_4,
    5: day_5,
    6: day_6,
    7: day_7
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
