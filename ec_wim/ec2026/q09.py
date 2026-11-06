from ecd import data
from collections import Counter


result = 0
for line in data["1"].splitlines():
    _, growth, limit = line.split(", ")
    growth = int(growth.split("=")[1])
    limit = int(limit.split("=")[1])
    t = size = n_splits = 0
    parts = Counter({0: 1})
    while size < limit:
        parts = Counter({k + 1: v for k, v in parts.items()})
        if growth in parts:
            n_split = parts.pop(growth)
            n_splits += n_split
            parts[1] += n_split
            parts[growth//2] += 2 * n_split
        size = sum(k * v for k, v in parts.items()) + n_splits
        t += 1
    result += t

print("Part 1:", result)


result = 0
for line in data["2"].splitlines():
    _, growth, limit = line.split(", ")
    growth = int(growth.split("=")[1])
    limit = int(limit.split("=")[1])
    t = n_splits = 0
    parts = Counter({0: 1})
    while n_splits + 1 < limit:
        t_inc = growth - max(parts)
        parts = Counter({k + t_inc: v for k, v in parts.items()})
        n_split = parts.pop(growth)
        n_splits += n_split
        parts[1] += n_split
        parts[growth//2] += 2 * n_split
        t += t_inc
    result += t

print("Part 2:", result)


result = 0
for line in data["3"].splitlines():
    _, growth, limit = line.split(", ")
    growth = int(growth.split("=")[1])
    limit = int(limit.split("=")[1])
    t = n_splits = 0
    parts = Counter({0: 1})
    while n_splits + 1 < limit:
        t_inc = growth - max(parts)
        parts = Counter({k + t_inc: v for k, v in parts.items()})
        n_split = parts.pop(growth)
        n_splits += n_split
        parts[1] += n_split
        parts[growth//2] += 2 * n_split
        t += t_inc
    result += t
    if not t:
        result += 1

print("Part 3:", result)
