from ecd import data
from math import isqrt

result = 0
for n in map(int, data["1"].split(",")):
    s = isqrt(n)
    s2 = s * s
    if s2 < n:
        result += (s + 1) * (s + 1) - n
print("Part 1:", result)

result = 0
for n in map(int, data["2"].split(",")):
    if n <= 8:
        result += 8 - n
        continue
    e = 1 + n // 4
    if 4 * (e - 1) < n:
        result += 4 * e - n
print("Part 2:", result)

result = 0
for n in map(int, data["3"].split(",")):
    if n <= 8:
        result += 8 - n
        continue
    s = isqrt(n + 1)
    s2 = s * s
    if s2 == n + 1 and s % 2:
        continue
    s += 2 if s % 2 else 1
    result += (s * s - 1) - n
print("Part 3:", result)
