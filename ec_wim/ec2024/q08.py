from ecd import data

N = int(data["1"])
n = 1
while n * n < N:
    n += 1
missing = n * n - N
width = 2 * n - 1
result = width * missing
print("Part 1:", result)

n_priests = int(data["2"])
n_acolytes = 1111
n_blocks = 20240000
thickness = count = layer = 1
while count < n_blocks:
    thickness *= n_priests
    thickness %= n_acolytes
    layer += 1
    width = 2 * layer - 1
    count += width * thickness
missing = count - n_blocks
result = width * missing
print("Part 2:", result)

n_priests = int(data["3"])
n_acolytes = 10
n_blocks = 202400000
thickness = count = layer = 1
thicknesses = [1]
while count < n_blocks:
    thickness *= n_priests
    thickness %= n_acolytes
    thickness += n_acolytes
    layer += 1
    width = 2 * layer - 1
    count += width * thickness
    thicknesses.append(thickness)
spaces = []
for col in range(layer - 1):
    n_space = n_priests * width
    n_space *= sum(thicknesses[col:])
    n_space %= n_acolytes
    spaces.append(n_space)
n_removed = spaces[0] + 2 * sum(spaces[1:])
result = count - n_removed - n_blocks
print("Part 3:", result)
