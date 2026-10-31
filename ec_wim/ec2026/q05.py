from ecd import data
from collections import Counter


def parsed(data):
    d = {}
    lines = data.splitlines()
    h = len(lines)
    [w] = {len(x) for x in lines}
    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            z = complex(x, y)
            d[z] = val
    mid = complex(w//2, h//2)
    d[mid] = "#"
    return d


def e1(d):
    dzs = [-1-1j, -1j, 1-1j, -1, 1, -1+1j, 1j, 1+1j]
    mutated = False
    for z, val in d.items():
        if val != "#":
            c = Counter(d.get(z + dz) for dz in dzs)
            if c["#"] >= 1 and c["#"] + c["1"] >= 5:
                d[z] = "#"
                mutated = True
    return mutated


def e2(d):
    dzs = [-1-1j, -1j, 1-1j, -1, 1, -1+1j, 1j, 1+1j]
    mutated = False
    for z, val in d.items():
        if val == "#":
            c = Counter(d.get(z + dz, "=") for dz in dzs)
            if c["="] >= 5:
                d[z] = "="
                mutated = True
    return mutated


def evolve(d, e):
    mutated = True
    while mutated:
        mutated = e(d)


def init_water(d):
    for z, val in d.items():
        if val in "01":
            d[z] = "."


def init_sand(d):
    dzs = [-1-1j, -1j, 1-1j, -1, 1, -1+1j, 1j, 1+1j]
    update = {}
    for z, val in d.items():
        if val == "#":
            c = Counter(d.get(z + dz, ".") for dz in dzs)
            if c["."]:
                update[z] = "="
    d.update(update)


def init_tree(d):
    exclude = {-2-2j, 2-2j, 0, -2+2j, 2+2j}
    dzs = [complex(x, y) for x in range(-2, 3) for y in range(-2, 3)]
    dzs = [z for z in dzs if z not in exclude]
    for z, val in d.items():
        if val == "#":
            c = Counter(d.get(z + dz, ".") for dz in dzs)
            if c["#"] + c["@"] == len(dzs):
                d[z] = "@"


def tree_grow(d):
    dzs = [-1-1j, -1j, 1-1j, -1, 1, -1+1j, 1j, 1+1j]
    update = {}
    for z, val in d.items():
        if val == "#":
            c = Counter(d.get(z + dz, ".") for dz in dzs)
            if c["@"] >= 4 and not c["="]:
                update[z] = "@"
    d.update(update)


for part in "123":
    d = parsed(data[part])
    evolve(d, e1)
    init_water(d)
    result = sum(v == "#" for v in d.values())
    if part == "1":
        print("Part 1:", result)
        continue

    init_sand(d)
    evolve(d, e2)
    result = sum(v == "=" for v in d.values())
    if part == "2":
        print("Part 2:", result)
        continue

    init_tree(d)
    tree_grow(d)
    tree_grow(d)
    result = sum(v == "@" for v in d.values())
    print("Part 3:", result)
