from ecd import data


track2 = """\
S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--
-                                                                     -
=                                                                     =
+                                                                     +
=                                                                     +
+                                                                     =
=                                                                     =
-                                                                     -
--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-
"""
track3 = """\
S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--
- + +   + =   =     =      =   == = - -     - =  =         =-=        -
= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++
+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=       
= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =          
+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==
=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =
-               = = = =   +  +  ==+ = = +   =        ++    =          -
-               = + + =   +  -  = + = = +   =        +     =          -
--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-
"""


tr = dict(zip("+=-S", (1, 0, -1, 0)))


def parse_track(raw):
    lines = raw.splitlines()
    lines = [f" {x} " for x in lines]
    [w] = {len(x) for x in lines}
    lines = [" " * w, *lines, " " * w]
    y0, x0 = 1, 1
    y1, x1 = 1, 2
    result = [lines[y1][x1]]
    while result[-1] != "S":
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            x = x1 + dx
            y = y1 + dy
            if (x, y) == (x0, y0):
                continue
            glyph = lines[y][x]
            if glyph != " ":
                x0, y0 = x1, y1
                x1, y1 = x, y
                result.append(glyph)
                break
    result = tuple([tr[x] for x in result])
    return result


def essence_score(track, path, memo={}):
    key = track, path
    if key in memo:
        return memo[key]
    p0 = p = 10
    psum = 0
    for i in range(len(track)):
        p += track[i] or path[i % len(path)]
        psum += p
    result = psum, (p - p0)
    memo[key] = result
    return result


def essence_laps(track, path, n=1):
    p = 0
    score = 0
    di = len(track) % len(path)
    for i in range(n):
        s, dp = essence_score(track, path)
        score += s + len(track) * p
        p += dp
        path = path[di:] + path[:di]
    return score


essence = {}
for line in data["1"].splitlines():
    pk, path = line.split(":")
    path = tuple([tr[x] for x in path.split(",")])
    essence[pk] = essence_laps((0,) * len(path), path, n=10)
result = "".join(sorted(essence, key=essence.get, reverse=True))
print(f"Part 1: {result}")

track = parse_track(track2)
scores2 = {}
for line in data["2"].splitlines():
    pk, path = line.split(":")
    path = tuple([tr[x] for x in path.split(",")])
    scores2[pk] = essence_laps(track, path, n=10)
result = "".join(sorted(scores2, key=scores2.get, reverse=True))
print(f"Part 2: {result}")

track = parse_track(track3)
path = tuple([tr[x] for x in data["3"].split(":")[1].split(",")])
rival_score = essence_laps(track, path, n=2024)
candidates = []
paths = [((), 5, 3, 3)]
while paths:
    path, n_plus, n_minus, n_equal = paths.pop()
    if len(path) == 11:
        candidates.append(path)
        continue
    if n_plus:
        paths.append((path + (1,), n_plus - 1, n_minus, n_equal))
    if n_minus:
        paths.append((path + (-1,), n_plus, n_minus - 1, n_equal))
    if n_equal:
        paths.append((path + (0,), n_plus, n_minus, n_equal - 1))
result = sum(essence_laps(track, x, n=2024) > rival_score for x in candidates)
print("Part 3:", result)
