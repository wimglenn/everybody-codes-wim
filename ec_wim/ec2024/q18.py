from ecd import data
from collections import deque


def parsed(data):
    space = set()
    palms = set()
    lines = data.splitlines()
    h = len(lines)
    [w] = {len(x) for x in lines}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            z = complex(x, y)
            if c == "P":
                space.add(z)
                palms.add(z)
            elif c == ".":
                space.add(z)
    return h, w, space, palms


def bfs(initial, space, palms):
    q = deque(initial)
    seen = set()
    watered = {}
    while len(watered) < len(palms):
        z0, t = q.popleft()
        if z0 in palms and z0 not in watered:
            watered[z0] = t
        if z0 not in seen:
            seen.add(z0)
            for dz in -1j, 1, 1j, -1:
                z1 = z0 + dz
                if z1 in space:
                    q.append((z1, t + 1))
    return max(watered.values())


_h, _w, space, palms = parsed(data["1"])
result = bfs([(1j, 0)], space, palms)
print("Part 1:", result)

h, w, space, palms = parsed(data["2"])
result = bfs([(1j, 0), (complex(w-1, h-2), 0)], space, palms)
print("Part 2:", result)


def shortest_paths(z0, space):
    q = deque([(z0, 0)])
    result = {}
    while q:
        z0, t = q.popleft()
        if z0 not in result:
            result[z0] = t
            for dz in -1j, 1, 1j, -1:
                z1 = z0 + dz
                if z1 in space:
                    q.append((z1, t + 1))
    return result


h, w, space, palms = parsed(data["3"])
paths = [shortest_paths(z0, space) for z0 in palms]
result = min(sum(p[z] for p in paths) for z in space if z not in palms)
print("Part 3:", result)
