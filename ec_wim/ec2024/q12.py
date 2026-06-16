from ecd import data


def parsed(data):
    lines = data.splitlines()[1:-1]
    lines = [x[1:] for x in reversed(lines)]
    assert lines[0][0] == "A"
    Ts = []
    Hs = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "T":
                Ts.append(complex(x, y))
            elif char == "H":
                Hs.append(complex(x, y))
    [w] = {len(x) for x in lines}
    return w, Hs, Ts


def trajectory(launcher, p, w):
    z = complex(0, launcher - 1)
    result = []
    for _ in range(p):
        z += 1 + 1j
        if z.real > w:
            return result
        result.append(z)
    for _ in range(p):
        z += 1
        if z.real > w:
            return result
        result.append(z)
    for _ in range(p + 3):
        z += 1 - 1j
        if z.real > w or z.imag < 0:
            return result
        result.append(z)
    return result


def gen_grid(w):
    grid = {}
    for power in range(1, w):
        for launcher in 3, 2, 1:
            for z in trajectory(launcher, power, w):
                score = launcher * power
                if grid.get(z, score) >= score:
                    grid[z] = score
    return grid


def solve(data):
    w, Hs, Ts = parsed(data)
    grid = gen_grid(w)
    result = sum(grid[z] for z in Ts)
    result += 2 * sum(grid[z] for z in Hs)
    return result


print("Part 1:", solve(data["1"]))
print("Part 2:", solve(data["2"]))


def intercept(z, grid):
    t = 0
    while z.imag > 0:
        t += 1
        z -= 1 + 1j
        if z in grid and z.real <= t:
            return grid[z]
    return 0


xys = [int(x) for x in data["3"].split()]
xs, ys = xys[0::2], xys[1::2]
zs = [complex(x, y) for x, y in zip(xs, ys)]
grid = gen_grid(1 + max(xs) // 2)
result = sum(intercept(z, grid) for z in zs)
print("Part 3:", result)
