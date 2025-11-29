from ecd import data


def runic_word(A, x0=0, y0=0):
    modified = False
    xs = range(x0 + 2, x0 + 6)
    ys = range(y0 + 2, y0 + 6)
    for y in ys:
        for x in xs:
            if A[y][x] != ".":
                continue
            seen = set()
            row = A[y][x0], A[y][x0 + 1], A[y][x0 + 6], A[y][x0 + 7]
            col = A[y0][x], A[y0 + 1][x], A[y0 + 6][x], A[y0 + 7][x]
            for c in row:
                if c == "?":
                    continue
                if c in col:
                    A[y][x] = c
                    modified = True
                    break
                seen.add(c)
    for y in ys:
        for x in xs:
            if A[y][x] == ".":
                d = {}
                for col in range(x0, x0 + 8):
                    d[y, col] = A[y][col]
                for row in range(y0, y0 + 8):
                    d[row, x] = A[row][x]
                counts = {}
                for c in d.values():
                    if c not in counts:
                        counts[c] = 1
                    else:
                        counts[c] += 1
                counts = {k: v for k, v in counts.items() if v != 2 or k == "."}
                if len(counts) == 3 and counts.get("?") == 1:
                    del counts["."]
                    del counts["?"]
                    [char] = counts
                    [(y_q, x_q)] = [k for (k, v) in d.items() if v == "?"]
                    A[y][x] = A[y_q][x_q] = char
                    modified = True
    result = "".join(A[y][x] for y in ys for x in xs)
    return result, modified


def power(word):
    return sum(i * (ord(x) - 64) for i, x in enumerate(word, 1))


A = [list(x) for x in data["1"].splitlines()]
result, _ = runic_word(A)
print("Part 1:", result)


lines = data["2"].splitlines()
col0 = "".join([x[:1] or " " for x in lines])
w = len(lines[0].split())
h = len(col0.split())
A = [list(x) for x in lines]
result = 0
for row in range(h):
    for col in range(w):
        word, _ = runic_word(A, x0=9 * col, y0=9 * row)
        result += power(word)
print("Part 2:", result)


lines = data["3"].splitlines()
col0 = "".join([x[0] for x in lines])
w = len(lines[0].strip("*").split("**"))
h = len(col0.strip("*").split("**"))
A = [list(x) for x in lines]
while True:
    result = 0
    count_modified = 0
    for row in range(h):
        for col in range(w):
            word, modified = runic_word(A, x0=6 * col, y0=6 * row)
            count_modified += modified
            if "." not in word:
                result += power(word)
    if not count_modified:
        break
print("Part 3:", result)
