from ecd import data


def p1_slow(ns, it=1):
    changed = False
    for _ in range(it):
        for i in range(1, len(ns)):
            if ns[i-1] > ns[i]:
                ns[i-1] -= 1
                ns[i] += 1
                changed = True
    return changed


def p2_slow(ns, it=1):
    changed = False
    for _ in range(it):
        for i in range(1, len(ns)):
            if ns[i] > ns[i - 1]:
                ns[i-1] += 1
                ns[i] -= 1
                changed = True
    return changed


def p2_fast(ns):
    q = sum(ns) // len(ns)
    result = 0
    for i in range(1, len(ns)):
        n_left = sum(ns[:i])
        diff = q * i - n_left
        if diff > result:
            result = diff
    return result


def checksum(ns):
    return sum(i * n for i, n in enumerate(ns, start=1))


ns = [int(x) for x in data["1"].split()]
r = 0
while p1_slow(ns):
    r += 1
p2_slow(ns, it=10-r)
print("Part 1:", checksum(ns))

for part in "23":
    ns = [int(x) for x in data[part].split()]
    r = 0
    while p1_slow(ns):
        r += 1
    r += p2_fast(ns)
    print(f"Part {part}:", r)
