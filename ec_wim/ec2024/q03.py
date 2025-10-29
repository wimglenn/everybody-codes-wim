from ecd import data

for part, raw in data.items():
    lines = raw.split()
    h = len(lines)
    [w] = {len(x) for x in lines}
    grid = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[complex(x, y)] = 0 if char == "." else 1
    result = raw.count("#")
    dzs = (0, 1, -1j, -1, 1j)
    if part == "3":  # include diagonals
        dzs += (-1 - 1j, 1 - 1j, 1 + 1j, -1 + 1j)
    while True:
        z_dig = {}
        for y in range(h):
            for x in range(w):
                z0 = complex(x, y)
                if not grid[z0]:
                    continue
                vals = [grid.get(z0 + dz, 0) for dz in dzs]
                d = dict.fromkeys(vals)
                if len(d) != 1:
                    continue
                [n] = d
                if not n:
                    continue
                z_dig[z0] = n + 1
        if not z_dig:
            break
        result += len(z_dig)
        grid.update(z_dig)
    print(f"Part {part}: {result}")
