from ecd import data
from heapq import nlargest


def parsed(data):
    stars = []
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == "*":
                stars.append((x, y))
    d = {}
    for i, (x0, y0) in enumerate(stars):
        for j, (x1, y1) in enumerate(stars[i+1:], start=i+1):
            d[i, j] = d[j, i] = abs(y0 - y1) + abs(x0 - x1)
    return len(stars), d


for part in "12":
    n, d = parsed(data[part])
    seen, dist = {0}, 0
    while len(seen) < n:
        unseen = {(i, j): v for (i, j), v in d.items() if i in seen and j not in seen}
        i, j = min(unseen, key=unseen.get)
        seen.add(j)
        dist += d[i, j]
    print(f"Part {part}:", n + dist)


n, d = parsed(data["3"])
d = {k: v for k, v in d.items() if v < 6}
remaining = range(n)
constellations = []
while remaining:
    seen, dist = {remaining[0]}, 0
    while True:
        unseen = {(i, j): v for (i, j), v in d.items() if i in seen and j not in seen}
        if not unseen:
            constellations.append(len(seen) + dist)
            remaining = [i for i in remaining if i not in seen]
            d = {(i, j): v for (i, j), v in d.items() if i not in seen and j not in seen}
            break
        i, j = min(unseen, key=unseen.get)
        seen.add(j)
        dist += d[i, j]
c0, c1, c2 = nlargest(3, constellations)
print("Part 3:", c0 * c1 * c2)
