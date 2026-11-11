from ecd import data


def parsed(data):
    LR, grid = data.split("\n\n")
    lines = grid.splitlines()
    h = len(lines)
    [w] = {len(x) for x in lines}
    d = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            z = complex(x, y)
            d[z] = c
    return h, w, LR, d


def decode(h, w, LR, d):
    dzs = [-1 - 1j, -1j, +1 - 1j, 1, 1 + 1j, 1j, -1 + 1j, -1]
    i = 0
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            z0 = complex(x, y)
            zs = [z0 + dz for dz in dzs]
            vals = [d[z] for z in zs]
            direction = LR[i % len(LR)]
            match direction:
                case "L":
                    vals = vals[1:] + [vals[0]]
                case "R":
                    vals = [vals[-1]] + vals[:-1]
            d.update(dict(zip(zs, vals)))
            i += 1


def get_message(h, w, d):
    zs = [complex(x, y) for y in range(h) for x in range(w)]
    s = "".join(d[z] for z in zs)
    return s[s.find(">")+1:s.find("<")]


h, w, LR, d = parsed(data["1"])
decode(h, w, LR, d)
get_message(h, w, d)
print("Part 1:", get_message(h, w, d))


h, w, LR, d = parsed(data["2"])
for _ in range(100):
    decode(h, w, LR, d)
print("Part 2:", get_message(h, w, d))


h, w, LR, d = parsed(data["3"])
zs = [complex(x, y) for y in range(h) for x in range(w)]
test0 = {z: i for i, z in enumerate(zs)}
test = test0.copy()
decode(h, w, LR, test)
test1 = {v: k for k, v in test.items()}
mapping = {k: test1[v] for k, v in test0.items()}
seen = set()
cycles = []
while len(seen) < len(mapping):
    z0 = next(z for z in mapping if z not in seen)
    cycle = [mapping[z0]]
    while z0 != cycle[-1]:
        cycle.append(mapping[cycle[-1]])
    cycles.append(cycle)
    seen.update(cycle)

N = 1_048_576_000
remap = {}
for cycle in cycles:
    i = N % len(cycle)
    rotated = cycle[i:] + cycle[:i]
    for z0, z1 in zip(cycle, rotated):
        remap[z1] = d[z0]
print("Part 3:", get_message(h, w, remap))
