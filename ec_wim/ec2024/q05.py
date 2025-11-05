from ecd import data

for part, raw in data.items():
    rows = raw.splitlines()
    ns = [[int(x) for x in row.split()] for row in rows]
    ns = [list(x)[::-1] for x in zip(*ns)]
    seen = set()
    counts = {}
    round = 0
    result1 = result2 = result3 = None
    while True:
        c0 = round % 4
        round += 1
        c1 = round % 4
        clapper = ns[c0].pop()
        n = len(ns[c1])
        q, r = divmod(clapper - 1, n)
        pos = r if q % 2 else (n - r)
        ns[c1].insert(pos, clapper)
        n0 = int("".join(map(str, [x[-1] for x in ns])))
        if round == 10 and part == "1":
            print("Part 1:", n0)
            break
        if n0 not in counts:
            counts[n0] = 0
        counts[n0] += 1
        if counts[n0] == 2024 and part == "2":
            print("Part 2:", round * n0)
            break
        if part == "3":
            state = c0, tuple(tuple(x) for x in ns)
            if state in seen:
                print("Part 3:", max(counts))
                break
            seen.add(state)
