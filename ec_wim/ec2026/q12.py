from ecd import data


def block_dims(block):
    x0 = int(min(z.real for z in block))
    y0 = int(min(z.imag for z in block))
    x1 = int(max(z.real for z in block))
    y1 = int(max(z.imag for z in block))
    W = x1 - x0 + 1
    H = y1 - y0 + 1
    if len(block) == W * H:
        # one rectangular block
        return [(W, H)]
    vs = [complex(x0, y0), complex(x0, y1), complex(x1, y0), complex(x1, y1)]
    if sum(v in block for v in vs) == 4:
        # block with a hole in it
        zs = [complex(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
        hole = [z for z in zs if z not in block]
        mx0 = int(min(z.real for z in hole))
        my0 = int(min(z.imag for z in hole))
        mx1 = int(max(z.real for z in hole))
        my1 = int(max(z.imag for z in hole))
        w = mx1 - mx0 + 1
        h = my1 - my0 + 1
        split1 = [(mx0 - x0, H), (w, my0 - y0), (w, y1 - my1), (x1 - mx1, H)]
        split2 = [(W, my0 - y0), (mx0 - x0, h), (x1 - mx1, h), (W, y1 - my1)]
    else:
        # L-shaped block
        w1 = sum(complex(x, y0) in block for x in range(x0, x1 + 1))
        w2 = sum(complex(x, y1) in block for x in range(x0, x1 + 1))
        h1 = sum(complex(x0, y) in block for y in range(y0, y1 + 1))
        h2 = sum(complex(x1, y) in block for y in range(y0, y1 + 1))
        w1, w2 = sorted([w1, w2])
        h1, h2 = sorted([h1, h2])
        split1 = [(w2, h1), (w1, h2 - h1)]
        split2 = [(w1, h2), (w2 - w1, h1)]
    if sum(map(min, split1)) < sum(map(min, split2)):
        return split1
    else:
        return split2


def parsed(data):
    lines = data.splitlines()
    zs = dict.fromkeys(complex(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#")
    seen = set()
    blocks = []
    for z in zs:
        if z in seen:
            continue
        block = set()
        stack = [z]
        while stack:
            z0 = stack.pop()
            if z0 not in block:
                block.add(z0)
                for dz in -1, -1j, 1, 1j:
                    z1 = z0 + dz
                    if z1 in zs:
                        stack.append(z1)
        seen.update(block)
        blocks += block_dims(block)
    return blocks


for part in "123":
    blocks = parsed(data[part])
    result = sum(min(b) for b in blocks)
    print(f"Part {part}:", result)
