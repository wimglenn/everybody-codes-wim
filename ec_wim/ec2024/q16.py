from ecd import data
import heapq
from collections import Counter


def parsed(data, part="1"):
    ns, rolls = data.split("\n\n")
    ns = [int(n) for n in ns.split(",")]
    stacks = [[] for _ in ns]
    for line in rolls.splitlines():
        for i, stack in enumerate(stacks):
            glyph = line[4*i:4*(i+1)].strip()
            if part != "1":
                glyph = glyph[::2]
            if glyph:
                stack.append(glyph)
    return ns, stacks


ns, stacks = parsed(data["1"])
ii = (0,) * len(ns)
for _ in range(100):
    ii = tuple((ii[i] + n) % len(stack) for i, (n, stack) in enumerate(zip(ns, stacks)))
result = " ".join([stack[i] for i, stack in zip(ii, stacks)])
print("Part 1:", result)


N = 202420242024
ns, stacks = parsed(data["2"], part="2")
ii = ii0 = (0,) * len(ns)
p = 0
coins = []
periodic = False
result = None
while not result:
    ii = tuple((ii[i] + n) % len(stack) for i, (n, stack) in enumerate(zip(ns, stacks)))
    p += 1
    counter = Counter([x for i, stack in zip(ii, stacks) for x in stack[i]])
    win = sum([c - 2 for c in counter.values() if c > 2])
    coins.append(win)
    if coins and ii == ii0:
        q, r = divmod(N - p, p)
        result = sum(coins) * (q + 1) + sum(coins[:r])
print("Part 2:", result)


def roll(ii, ns, stacks, offset=0):
    return tuple((ii[i] + n + offset) % len(stack) for i, (n, stack) in enumerate(zip(ns, stacks)))


def score(ii, stacks):
    counter = Counter([x for i, stack in zip(ii, stacks) for x in stack[i]])
    win = sum([c - 2 for c in counter.values() if c > 2])
    return win


def search(p, ns, stacks, max_heap=False):
    f = -1 if max_heap else 1
    m = -4 if max_heap else 0  # because 4 is the most coins per pull e.g. ^_^ ^_^ ^.^
    best = {}
    pq = [(0, 0, p, (0,) * len(ns))]  # min-heap (coins, pulls remaining, position)
    while pq:
        _, coins0, pulls0, ii0 = heapq.heappop(pq)
        if not pulls0:
            return coins0 * f
        if best.get((pulls0, ii0), coins0 + 1) > coins0:
            best[pulls0, ii0] = coins0
            for offset in (-1, 0, 1):
                ii1 = roll(ii0, ns, stacks, offset=offset)
                coins1 = coins0 + score(ii1, stacks) * f
                pulls1 = pulls0 - 1
                priority = coins1 + (pulls0 - 1) * m
                heapq.heappush(pq, (priority, coins1, pulls1, ii1))


N = 256
ns, stacks = parsed(data["3"], part="3")
min_c = search(N, ns, stacks)
max_c = search(N, ns, stacks, max_heap=True)
print(f"Part 3: {max_c} {min_c}")
