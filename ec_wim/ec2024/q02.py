from ecd import data

words, inscription = data["1"].split("\n\n")
words = words.split(":")[1].split(",")
n1 = sum(inscription.count(x) for x in words)
print(f"Part 1: {n1}")

words, inscription = data["2"].split("\n\n")
words = words.split(":")[1].split(",")
words_set = set(words)
words_length = [len(x) for x in words]
min_len = min(words_length)
max_len = max(words_length)
words_set.update([x[::-1] for x in words])  # search for runic words in both directions
runic_symbols = [0] * len(inscription)
for k in range(min_len, max_len + 1):
    for i in range(len(inscription)):
        s = inscription[i : i + k]
        if s in words_set:
            for j in range(i, i + len(s)):
                runic_symbols[j] = 1
n2 = sum(runic_symbols)
print(f"Part 2: {n2}")

words, inscription = data["3"].split("\n\n")
words = words.split(":")[1].split(",")
words_set = set(words)
words_length = [len(x) for x in words]
min_len = min(words_length)
max_len = max(words_length)
words_set.update([x[::-1] for x in words])  # search for runic words in both directions
lines = inscription.splitlines()
h = len(lines)
[w] = {len(x) for x in lines}
runic_symbols = set()
grid = {}
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        grid[complex(x, y)] = char
for k in range(min_len, max_len + 1):
    for y in range(h):
        for x in range(w):
            zx = [complex((x + i) % w, y) for i in range(k)]  # horizontals wrap
            zy = [complex(x, y + i) for i in range(k) if y + i < h]  # verticals don't
            sx = "".join(grid[z] for z in zx)
            sy = "".join(grid[z] for z in zy)
            if sx in words_set:
                runic_symbols.update(zx)
            if sy in words_set:
                runic_symbols.update(zy)
n3 = len(runic_symbols)
print(f"Part 3: {n3}")
