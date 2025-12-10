from itertools import product
from scipy.optimize import linprog


print("Day 10")
EXAMPLE = False


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


print("Part 1:", solution := part_1())
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


print("Part 2:", solution := part_2())
assert solution == (33 if EXAMPLE else 18387)
