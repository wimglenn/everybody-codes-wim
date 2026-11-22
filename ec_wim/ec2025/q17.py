import heapq
import itertools as it
from ecd import data


def parsed(data):
    d = {}
    lines = data.replace("@", "0").splitlines()
    R = len(lines) // 2
    offset = -complex(R, R)
    S = None
    for y, line in enumerate(lines):
        for x, n in enumerate(line):
            z = complex(x, y)
            if n == "S":
                S = z + offset
                n = "0"
            d[z + offset] = int(n)
    return S, R, d

_, _, d = parsed(data["1"])
result = sum(n for z, n in d.items() if abs(z) <= 10)
print("Part 1:", result)


_, R, d = parsed(data["2"])
results = {}
for r in range(R):
    destroyed = [n for z, n in d.items() if r < abs(z) <= r + 1]
    results[r + 1] = sum(destroyed)
r = max(results, key=results.get)
result = r * results[r]
print("Part 2:", result)


result = None
S, R, d = parsed(data["3"])
tie = it.count()
for r in range(R):  # volcano size
    T = 30 * (r + 1)  # time limit to complete loop within this radius
    targets = {}
    for f in -1, 1:  # path direction clockwise, anticlockwise
        seen = {}  # best time to reach node
        pq = [(0, next(tie), S)]
        while pq:
            t0, _i, z0 = heapq.heappop(pq)
            if t0 >= T:  # path too slow, prune
                continue
            if z0 not in seen:
                seen[z0] = t0
                for dz in -1, -1j, 1, 1j:
                    z1 = z0 + dz
                    if z1 not in d:  # outside grid
                        continue
                    if abs(z1) <= r:  # in volcano
                        continue
                    if f == -1 and z1.real < -r:  # trying to go anticlockwise
                        continue
                    if f == 1 and z1.real > r:  # trying to go clockwise
                        continue
                    t1 = t0 + d[z1]
                    heapq.heappush(pq, (t1, next(tie), z1))
        targets[f] = {z: t for z, t in seen.items() if z.real == 0 and z.imag > 0}
    zs = targets[-1].keys() & targets[1].keys()  # bottom half of middle column
    loop_times = [targets[-1][z] + targets[1][z] - d[z] for z in zs]
    if any(t < T for t in loop_times):
        result = min(loop_times) * r
        break
print("Part 3:", result)
