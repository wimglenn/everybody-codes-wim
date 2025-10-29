from ecd import data

d = dict(zip("ABCD", [0, 1, 3, 5]))
for part, S in data.items():
    part = int(part)
    result = 0
    for i in range(0, len(S), part):
        s = S[i : i + part].replace("x", "")
        for c in s:
            result += len(s) - 1 + d[c]
    print(f"Part {part}: {result}")
