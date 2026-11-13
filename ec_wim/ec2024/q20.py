from ecd import data
import heapq
import itertools as it
from collections import defaultdict


def parsed(data):
    lines = data.splitlines()
    space = set()
    plus = set()
    minus = set()
    goals = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            z = complex(x, y)
            if c == "#":
                continue
            space.add(z)
            if c == "+":
                plus.add(z)
            elif c == "-":
                minus.add(z)
            elif c != ".":
                goals[c] = z
    goals = dict(sorted(goals.items()))
    return space, plus, minus, goals


space, plus, minus, goals = parsed(data["1"])
# altitude, time remaining, tiebreak (int), prev pos (complex), current pos (complex)
pq = [(1000, 100, -1, -1j, goals["S"])]
best = {}
tie = it.count()
while pq:
    h0, t0, _tie, z_prev, z0 = heapq.heappop_max(pq)
    key = t0, z_prev, z0
    if best.get(key, h0 - 1) < h0:
        best[key] = h0
        if t0 > 0:
            t1 = t0 - 1
            for dz in -1j, 1, 1j, -1:
                z1 = z0 + dz
                if z1 in space and z1 != z_prev:
                    if z1 in plus:
                        h1 = h0 + 1
                    elif z1 in minus:
                        h1 = h0 - 2
                    else:
                        h1 = h0 - 1
                    heapq.heappush_max(pq, (h1, t1, next(tie), z0, z1))

result = max([h for (t, _, _), h in best.items() if t == 0])
print("Part 1:", result)


def path_generator(z_prev, z_start, z_target, plus, minus, space):
    seen = defaultdict(list)
    tie = it.count()
    # time, altitude loss, tiebreaker, prev pos, current pos
    pq = [(0, 0, next(tie), z_prev, z_start)]
    while pq:
        t0, dh0, _, z_prev, z0 = heapq.heappop(pq)
        k = z_prev, z0
        if k in seen and any((t <= t0 and dh <= dh0) for t, dh in seen[k]):
            continue
        seen[k].append((t0, dh0))
        if z0 == z_target:
            yield t0, dh0
        t1 = t0 + 1
        for dz in -1j, 1, 1j, -1:
            z1 = z0 + dz
            if z1 not in space or z1 == z_prev:
                continue
            if z1 in plus:
                dh1 = dh0 - 1
            elif z1 in minus:
                dh1 = dh0 + 2
            else:
                dh1 = dh0 + 1
            heapq.heappush(pq, (t1, dh1, next(tie), z0, z1))


space, plus, minus, goals = parsed(data["2"])
path_gens = {}
path_gens["SA"] = path_generator(goals["S"] - 1j, goals["S"], goals["A"], plus, minus, space)
path_gens["AB"] = path_generator(goals["A"] - 1j, goals["A"], goals["B"], plus, minus, space)
path_gens["BC"] = path_generator(goals["B"] + 1j, goals["B"], goals["C"], plus, minus, space)
path_gens["CS"] = path_generator(goals["C"] - 1, goals["C"], goals["S"], plus, minus, space)
search_depth = {
    "SA": 50,
    "AB": 60,
    "BC": 20,
    "CS": 40,
}
paths = {}
for k, v in search_depth.items():
    paths[k] = [next(path_gens[k]) for _ in range(v)]
result = None
for p in it.product(*paths.values()):
    dh = sum(x[1] for x in p)
    if dh > 0:
        # too much altitude loss
        continue
    t = sum(x[0] for x in p)
    if result is None or t < result:
        result = t
print("Part 2:", result)


space, plus, minus, goals = parsed(data["3"])
z0 = goals["S"]
zP = min(plus, key=lambda z: abs(z - z0))
dx0 = int(abs(z0.real - zP.real))
dy0 = int(abs(z0.imag - zP.imag))
h = 384_400
result = 0
h -= dx0
while h:
    result += 1
    h += -1 if (result - dy0) % 4 else 1
print("Part 3:", result)
