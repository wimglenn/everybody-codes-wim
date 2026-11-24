from ecd import data


def n_flaps(x, y):
    return (x - y) // 2 + y


def key(ys):
    # sort key - leftmost first, then shortest
    return ys[0], ys[1] - ys[0]


def merge(y_range):
    result = []
    for y0, y1 in sorted(y_range, key=key):
        if not result:
            result.append([y0, y1])
            continue
        y0_prev, y1_prev = result[-1]
        if y0 <= y1_prev:
            result[-1][1] = max(y1_prev, y1)
        else:
            result.append([y0, y1])
    return result


def intersect2(a, b):
    a, b = sorted([a, b], key=key)
    a0, a1 = a
    b0, b1 = b
    if a1 < b0:
        return None
    return [max(a0, b0), min(a1, b1)]


def intersect(ys0, ys1):
    result = []
    for y1 in ys1:
        for y0 in ys0:
            i = intersect2(y0, y1)
            if i is not None:
                result.append(i)
    return result


for part in "123":
    xs = [0]
    ys = [[[0, 0]]]
    for line in data[part].splitlines():
        x, y, h = [int(x) for x in line.split(",")]
        r_y = [y, y + h - 1]
        if r_y[0] % 2 != x % 2:
            r_y[0] += 1
        if r_y[1] % 2 != x % 2:
            r_y[1] -= 1
        if x == xs[-1]:
            ys[-1].append(r_y)
        else:
            xs.append(x)
            ys.append([r_y])

    for i in range(1, len(xs)):
        y_prevs = ys[i - 1]
        dx = xs[i] - xs[i-1]
        y_next = []
        for y_min, y_max in y_prevs:
            y_range = [y_min - dx, y_max + dx]
            if y_range[0] <= 0:
                y_range[0] = xs[i] % 2
            y_next.append(y_range)
        y_next = merge(y_next)
        ys[i] = intersect(y_next, ys[i])

    x = xs[-1]
    y = ys[-1][0][0]
    print(f"Part {part}:", n_flaps(x, y))
