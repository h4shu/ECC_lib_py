import random

PRIME = 2**13 - 1

class Fq(int):
    q = PRIME
    def __init__(self, a: int):
        self = a % Fq.q

    def __add__(self, other):
        return Fq((int(self) + int(other)) % Fq.q)

    def __sub__(self, other):
        return Fq((int(self) - int(other)) % Fq.q)

    def __mul__(self, other):
        return Fq((int(self) * int(other)) % Fq.q)

    def __truediv__(self, other):
        return Fq((int(self) * int(other.inv())) % Fq.q)

    def __pow__(self, e):
        return Fq(pow(int(self), int(e), Fq.q))

    def inv(self):
            a = int(self)
            m = Fq.q
            abs_m = -m if m < 0 else m
            b = m
            x = 1
            u = 0
            while b > 0:
                    q = a // b
                    tmp = u
                    u = x - q * u
                    x = tmp
                    tmp = b
                    b = a - q * b
                    a = tmp
            return abs_m + x if x < 0 else x

    def lds(self):
            if self == 0:
                    return 0
            x = int(self)
            y = Fq.q
            L = 1
            while True:
                    x = x % y
                    if x > y // 2:
                            x = y - x
                            if y % 4 == 3:
                                    L = -L
                    while x % 4 == 0:
                            x = x // 4
                    if x % 2 == 0:
                            x = x // 2
                            tmp = y % 8
                            if tmp == 3 or tmp == 5:
                                    L = -L
                    if x == 1:
                            return L
                    elif x % 4 == 3 and y % 4 == 3:
                            L = -L
                    tmp = x
                    x = y
                    y = tmp

    def sqrt(self):
            if Fq.q % 4 == 3:
                    return self ** ((Fq.q + 1) >> 2)

            p = Fq.q - 1
            e = 0
            while p % 2 == 0:
                    e += 1
                    p >>= 1
            while True:
                    n = Fq.rand()
                    if n.lds() == -1:
                            break
            y = n ** p
            x = self ** ((p - 1) >> 1)
            b = self * (x ** 2)
            x = self * x

            while b != 1:
                    m = 0
                    while True:
                            m = m + 1
                            tmp = b
                            tmp = tmp ** (2 ** m)
                            if tmp == 1:
                                    break
                    t = y ** (2 ** (e - m - 1))
                    y = t ** 2
                    x = x * t
                    b = b * y
                    e = m
            return x

    @staticmethod
    def rand():
            return Fq(random.randrange(Fq.q))

