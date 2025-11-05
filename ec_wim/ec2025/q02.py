from ecd import data


class Complex:

    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    @classmethod
    def fromstr(cls, s):
        return cls(*map(int, s.split("=")[-1].strip("[]").split(",")))

    def __str__(self):
        return f"[{self.real},{self.imag}]"

    def __add__(self, other):
        real = self.real + other.real
        imag = self.imag + other.imag
        result = Complex(real, imag)
        return result

    def __mul__(self, other):
        real = self.real * other.real - self.imag * other.imag
        imag = self.real * other.imag + other.real * self.imag
        result = Complex(real, imag)
        return result

    def __floordiv__(self, other):
        real = abs(self.real) // other.real
        imag = abs(self.imag) // other.imag
        if self.real < 0:
            real *= -1
        if self.imag < 0:
            imag *= -1
        result = Complex(real, imag)
        return result


def f(z, A, d=Complex(100_000, 100_000)):
    z *= z
    z //= d
    z += A
    return z


def engrave(a):
    z = Complex(0, 0)
    for i in range(100):
        z = f(z, a)
        if abs(z.real) > 1_000_000 or abs(z.imag) > 1_000_000:
            return False
    return True


A1 = Complex.fromstr(data["1"])
z = Complex(0, 0)
for i in range(3):
    z = f(z, A1, d=Complex(10, 10))
print("Part 1:", z)

A2 = Complex.fromstr(data["2"])
r2 = range(0, 1001, 10)
print("Part 2:", sum(engrave(A2 + Complex(x, y)) for y in r2 for x in r2))

A3 = Complex.fromstr(data["3"])
r3 = range(1001)
print("Part 3:", sum(engrave(A3 + Complex(x, y)) for y in r3 for x in r3))
