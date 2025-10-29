from ecd import data

for part, ns in data.items():
    nails = sorted([int(x) for x in ns.split()])
    dx = nails[0] if part in "12" else nails[len(nails) // 2]
    result = sum(abs(x - dx) for x in nails)
    print(f"Part {part}: {result}")
