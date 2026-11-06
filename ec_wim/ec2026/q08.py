from ecd import data


def parse_grid(data):
    d = {}
    lines = data.split()

    zz_diag = []
    zz_antidiag = []
    zz_lr = []

    for y, row in enumerate(lines):
        z_row = []
        for x, val in enumerate(row):
            if val == ".":
                continue
            z = complex(x, y)
            d[z] = int(val)
            z_row.append(z)
        zz_lr.append(z_row)

    z0 = complex(0, len(lines) // 2)
    dz = 1 + 1j
    while True:
        z = z0
        zs = [z]
        while z + dz in d:
            z += dz
            zs.append(z)
        zz_diag.append(zs)
        z0 += 1 - 1j
        if z0 not in d:
            z0 += 1 + 1j
            if z0 not in d:
                break

    z0 = next(iter(d))
    dz = -1 + 1j
    while True:
        z = z0
        zs = [z]
        while z + dz in d:
            z += dz
            zs.append(z)
        zz_antidiag.append(zs)
        z0 += 2
        if z0 not in d:
            z0 += dz
            if z0 not in d:
                break

    return zz_diag, zz_antidiag, zz_lr, d


def part1(zz, grid):
    result = 0
    for zs in zz:
        shadow = 0
        for z in zs:
            shadow -= 1
            if shadow < grid[z]:
                shadow = grid[z]
                result += 1
    return result


zz, _, _, grid = parse_grid(data["1"])
print("Part 1:", part1(zz, grid))

zz_diag, zz_antidiag, zz_lr, grid = parse_grid(data["2"])
# 6 directions  ↘ ↙ ← ↖ ↗ →
dirs = [
    zz_diag,
    zz_antidiag,
    [zs[::-1] for zs in zz_lr],
    [zs[::-1] for zs in zz_diag],
    [zs[::-1] for zs in zz_antidiag],
    zz_lr,
]
result = sum(part1(x, grid) for x in dirs)
print("Part 2:", result)


def evolve(zz, grid):
    n_warriors = 0
    result = 0
    for zs in zz:
        shadow = 0
        for z in zs:
            shadow -= 1
            if grid[z] <= 0:
                grid[z] += 1
                continue
            if shadow < grid[z]:
                shadow = grid[z]
                if grid[z] == 9:
                    n_warriors += 1
                    grid[z] = -2
                else:
                    grid[z] += 1
                result += 1
    return result, n_warriors


_, _, _, grid = parse_grid(data["3"])
i = n_warriors = result = 0
while n_warriors < 100_000:
    r, n = evolve(dirs[i % 6], grid)
    i += 1
    result += r
    n_warriors += n

print("Part 3:", result)
