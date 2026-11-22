from ecd import data
import math


ns = [int(x) for x in data["1"].split(",")]
result = 0
for n in ns:
    q, r = divmod(90, n)
    result += q
print("Part 1:", result)


def get_spells(ns):
    ns = ns[:]
    spells = []
    while any(ns):
        spell = None
        for i, n in enumerate(ns):
            if n > 0:
                if spell is None:
                    spell = i + 1
                    spells.append(spell)
            if spell is not None and (i + 1) % spell == 0:
                ns[i] -= 1
    return spells


ns = [int(x) for x in data["2"].split(",")]
result = math.prod(get_spells(ns))
print("Part 2:", result)


ns = [int(x) for x in data["3"].split(",")]
N = 2025_2025_2025_000
spells = get_spells(ns)
lo = len(ns)
hi = N
while hi - lo > 1:
    mid = (lo + hi) // 2
    n = sum(mid // x for x in spells)
    if n <= N:
        lo = mid
    else:
        hi = mid
print("Part 3:", lo)
