from collections import deque
from ecd import data


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __abs__(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __mul__(self, f):
        return Vector3(f * self.x, f * self.y, f * self.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"


F = Vector3(x=1)
R = Vector3(y=1)
U = Vector3(z=1)
unit_vectors = dict(zip("UDRLFB", [U, -U, R, -R, F, -F]))


def grow(line):
    v = Vector3()
    seen = set()
    for step in line.split(","):
        u = unit_vectors[step[0]]
        for _ in range(int(step[1:])):
            v += u
            seen.add(v)
    return seen


seen = grow(data["1"])
print("Part 1:", max(x.z for x in seen))

seen = set()
for line in data["2"].splitlines():
    seen.update(grow(line))
print("Part 2:", len(seen))


def bfs(vs, start, end):
    q = deque([(start, 0)])
    seen = {start}
    while q:
        v0, d0 = q.popleft()
        for dv in unit_vectors.values():
            v1 = v0 + dv
            d1 = d0 + 1
            if v1 == end:
                return d1
            if v1 not in seen and v1 in vs:
                seen.add(v1)
                q.append((v1, d1))


v = Vector3()
seen = set()
leaf = set()
for line in data["3"].splitlines():
    v = Vector3()
    for step in line.split(","):
        u = unit_vectors[step[0]]
        for _ in range(int(step[1:])):
            v += u
            seen.add(v)
    leaf.add(v)
trunk = {x for x in seen if x.x == 0 and x.y == 0}
min_murkiness = None
for t in trunk:
    murkiness = sum(bfs(vs=seen, start=t, end=x) for x in leaf)
    if min_murkiness is None or murkiness < min_murkiness:
        min_murkiness = murkiness
print("Part 3:", min_murkiness)
