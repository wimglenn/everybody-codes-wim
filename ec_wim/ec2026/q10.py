from ecd import data
from collections import Counter


def parsed(data):
    g_zs = []  # ghost positions
    g_dz = []  # ghost directions
    g_cc = []  # ghost collision counter
    chamber = set()
    dzs = dict(zip(">v<^", (1, 1j, -1, -1j)))
    for y, row in enumerate(data.splitlines()):
        for x, c in enumerate(row):
            z = complex(x, y)
            if c != "#":
                chamber.add(z)
            if c in dzs:
                g_zs.append(z)
                g_dz.append(dzs[c])
                g_cc.append(0)
    return g_zs, g_dz, g_cc, chamber


def evolve(g_zs, g_dz, g_cc, chamber, collision_limit=10_000):
    wall_collisions = []
    for i, (z0, dz) in enumerate(zip(g_zs, g_dz)):
        if z0 is None:
            continue
        if z0 + dz in chamber:
            g_zs[i] += dz
        else:
            g_dz[i] *= 1j
            wall_collisions.append(i)
    for i in wall_collisions:
        g_cc[i] += 1
        if g_cc[i] == collision_limit:
            g_zs[i] = g_dz[i] = None
    zs_occupied = Counter(g_zs)
    for i, (z0, dz) in enumerate(zip(g_zs, g_dz)):
        if z0 is None:
            continue
        if zs_occupied[z0] > 1:
            g_dz[i] *= -1
            g_cc[i] += 1
            if g_cc[i] == collision_limit:
                g_zs[i] = g_dz[i] = None


def evolve_with_cache(g_zs, g_dz, g_cc, chamber, collision_limit=1_000_000_000_000):
    memo = {}
    cycles = {}
    i = 0
    while any(g_zs):
        k = tuple(g_zs), tuple(g_dz)
        if k in cycles:
            inc_i, inc_cc = cycles[k]
            # figure out how many times we can go around the cycle
            # without any ghost going over their collision limit
            fs = []
            for n, dn in zip(g_cc, inc_cc):
                if dn > 0:
                    fs.append((collision_limit - n - 1) // dn)
            if fs and all(f > 0 for f in fs):
                f = min(fs)
                i += f * inc_i
                g_cc[:] = [n + f * dn for n, dn in zip(g_cc, inc_cc)]
        elif k in memo:
            i_prev, g_cc_prev = memo[k]
            inc_i = i - i_prev
            inc_cc = [y - x for x, y in zip(g_cc_prev, g_cc)]
            cycles[k] = inc_i, inc_cc
        else:
            memo[k] = i, tuple(g_cc)
        evolve(g_zs, g_dz, g_cc, chamber, collision_limit=collision_limit)
        i += 1
    return i


g_zs, g_dz, g_cc, chamber = parsed(data["1"])
for i in range(10):
    evolve(g_zs, g_dz, g_cc, chamber)
print("Part 1:", sum(g_cc))

g_zs, g_dz, g_cc, chamber = parsed(data["2"])
result = evolve_with_cache(g_zs, g_dz, g_cc, chamber, collision_limit=10_000)
print("Part 2:", result)

g_zs, g_dz, g_cc, chamber = parsed(data["3"])
result = evolve_with_cache(g_zs, g_dz, g_cc, chamber)
print("Part 3:", result)
