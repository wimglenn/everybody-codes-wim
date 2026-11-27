import math
from ecd import data


def parsed1(chunk):
    d = []
    for line in chunk.splitlines():
        d.append([int(x) for x in line.split()[-1].split(":")])
    F = math.lcm(*d[0])
    fs = [F // x for x in d[0]]
    d[1] = [f * x for f, x in zip(fs, d[1])]
    d[2] = [f * x for f, x in zip(fs, d[2])]
    d = list(zip(*d))
    return F, d


def parsed(data):
    chunks = data.replace("CCW", "-1").replace("CW", "1").split("\n\n")
    return [parsed1(x) for x in chunks]


def count_pair(F, c0, c1, d0, d1, m):
    if d1 < 0:
        # wlog, make hand 1 be rotating clockwise
        return count_pair(F, F - c0, F - c1, -d0, -d1, m)
    if c0 != 0:
        # wlog, make hand 0 be pointing at 12 o'clock
        return count_pair(F, 0, (c1 - c0) % F, d0, d1, m)
    if d1 < d0:
        # wlog, make hand 1 the faster one
        return count_pair(F, c1, c0, d1, d0, m)
    if d0 != 0:
        # wlog, make hand 0 stationary
        return count_pair(F, c0, c1, 0, d1 - d0, m)
    result, rem = divmod(d1 * m, F)
    result += c1 + rem >= F
    return result


def count_intersections(clocks):
    result = 0
    for F, d in clocks:
        r = 0
        pairs = [(i, j) for i in range(3) for j in range(i + 1, 3)]
        for i0, i1 in pairs:
            if d[i0][-1] > d[i1][-1]:
                i0, i1 = i1, i0  # put the hand that stops earliest first
            h0, d0, c0, m0 = d[i0]
            h1, d1, c1, m1 = d[i1]
            r += count_pair(F, c0, c1, d0, d1, m0)
            c0 = (c0 + m0 * d0) % F
            c1 = (c1 + m0 * d1) % F
            r += count_pair(F, c0, c1, 0, d1, m1 - m0)
        result += r
    return result


for part in "123":
    clocks = parsed(data[part])
    result = count_intersections(clocks)
    print(f"Part {part}:", result)
