from ecd import data

first, *_, last = data["1"].split()
result1 = 2025 * int(first) // int(last)
print(f"Part 1:", result1)

first, *_, last = data["2"].split()
f = 10_000_000_000_000 * int(last) / int(first)
if f != int(f):  # ceil
    f += 1
result2 = int(f)
print(f"Part 2:", result2)

first, *pairs, last = data["3"].split()
n = int(first)
d = int(last)
for pair in pairs:
    x, y = map(int, pair.split("|"))
    n *= y
    d *= x
result3 = 100 * n // d
print("Part 3:", result3)
