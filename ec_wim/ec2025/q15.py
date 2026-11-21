from collections import deque
from ecd import data


def vertices_to_wall(vertices):
    wall = set()
    for z0, z1 in zip(vertices, vertices[1:]):
        if z0.real == z1.real:
            y0, y1 = sorted([int(z0.imag), int(z1.imag)])
            wall.update([complex(z0.real, y) for y in range(y0, y1 + 1)])
        else:
            x0, x1 = sorted([int(z0.real), int(z1.real)])
            wall.update([complex(x, z0.imag) for x in range(x0, x1 + 1)])
    return wall


def bfs_compressed(wall, target, start, compressed_x, compressed_y):
    x_min = min(z.real for z in wall) - 1
    x_max = max(z.real for z in wall) + 1
    y_min = min(z.imag for z in wall) - 1
    y_max = max(z.imag for z in wall) + 1
    seen = set()
    q = deque([(start, 0, 0, 0)])
    while q:
        z0, d0, comp_x0, comp_y0 = q.popleft()
        if z0 == target:
            return d0
        if z0 not in seen:
            seen.add(z0)
            for dz in -1, -1j, 1, 1j:
                z1 = z0 + dz
                if not (x_min <= z1.real <= x_max and y_min <= z1.imag <= y_max):
                    continue
                if z1 not in wall:
                    d1 = d0 + 1
                    if dz.real:  # moving horizontally
                        comp_x1 = 0 if comp_x0 else dz
                        comp_y1 = comp_y0
                        if comp_x0 == dz:
                            d1 += compressed_x[int(z0.real)] - 1
                    else:  # moving vertically
                        comp_x1 = comp_x0
                        comp_y1 = 0 if comp_y0 else dz
                        if comp_y0 == dz:
                            d1 += compressed_y[int(z0.imag)] - 1
                    q.append((z1, d1, comp_x1, comp_y1))


for part in "123":
    steps = data[part].split(",")
    z, dz = 0, -1j
    vertices = [0]
    for step in steps:
        dz *= 1j if step[0] == "R" else -1j
        n = int(step[1:])
        z += n * dz
        vertices.append(z)

    xs = [int(z.real) for z in vertices]
    ys = [int(z.imag) for z in vertices]
    xs = sorted(dict.fromkeys(xs))  # order-preserving unique
    ys = sorted(dict.fromkeys(ys))

    # coordinate compression
    xd = {x: 2*i+1 for i, x in enumerate(xs)}
    yd = {y: 2*i+1 for i, y in enumerate(ys)}
    xdi = {k: v for v, k in xd.items()}
    ydi = {k: v for v, k in yd.items()}

    vd = [complex(xd[z.real], yd[z.imag]) for z in vertices]
    xs_d = [int(z.real) for z in vd]
    ys_d = [int(z.imag) for z in vd]

    start = vd[0]
    target = vd[-1]
    wall = vertices_to_wall(vd)
    wall.discard(target)

    compressed_x = {}
    compressed_y = {}
    xdiv = list(xdi.values())
    ydiv = list(ydi.values())
    for i, (y0, y1) in enumerate(zip(ydiv, ydiv[1:])):
        compressed_y[2*i + 2] = y1 - y0 - 1
    for i, (x0, x1) in enumerate(zip(xdiv, xdiv[1:])):
        compressed_x[2*i + 2] = x1 - x0 - 1

    result = bfs_compressed(wall, target, start, compressed_x, compressed_y)
    print(f"Part {part}:", result)
