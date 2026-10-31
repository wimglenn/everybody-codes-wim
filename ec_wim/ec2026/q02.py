from collections import defaultdict
from ecd import data
from functools import cmp_to_key

for part in "123":
    result = 0
    for line in data[part].splitlines():
        d = defaultdict(set)

        for xy in line.split():
            if "<" in xy:
                x, y = xy.split("<")
            elif ">" in xy:
                y, x = xy.split(">")
            d[x].add(y)
            d[y]

        for k, vs in d.items():
            for v in list(vs):
                d[k] |= d[v]

        def cmp(a, b):
            if b in d[a]:
                return 1
            elif a in d[b]:
                return -1

        result += int("".join(sorted(d, key=cmp_to_key(cmp))))

    print(f"Part {part}:", result)
