from ecd import data

A = result = 0
for a in data["1"]:
    A += a == "A"
    if a == "a":
        result += A
print("Part 1:", result)

count = dict.fromkeys("ABC", 0)
result = 0
for x in data["2"]:
    if x in count:
        count[x] += 1
    else:
        result += count[x.upper()]
print("Part 2:", result)

d = 1000
r = 1000
s = data["3"] * r
result = 0
for i, x in enumerate(s):
    if x not in "abc":
        continue
    X = x.upper()
    result += s[max(i - d, 0) : (i + d + 1)].count(X)
print("Part 3:", result)
