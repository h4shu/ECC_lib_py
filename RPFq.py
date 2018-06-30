from Fq import Fq

class RPFq:
    X = 2 ** 114 + 2 ** 101 - 2 ** 14 - 1
    Fq.q = 36 * (X ** 4) + 36 * (X ** 3) + 24 * (X ** 2) + 6 * X + 1
    t = 6 * (X ** 2) + 1
    r = 36 * (X ** 4) + 36 * (X ** 3) + 18 * (X ** 2) + 6 * X + 1
    a = Fq(0)
    b = Fq(2)

    def __init__(self, _x: Fq, _y: Fq):
        self.x = Fq(_x)
        self.y = Fq(_y)
        self.__z = 1

    def set_infinity(self):
        self.__x = Fq(0)
        self.__y = Fq(0)
        self.__z = 0

    def __add__(P, Q):
        R = RPFq(0, 0)
        l = Fq(0)
        if P.__z == 0 and Q.__z == 0:
            R.set_infinity()
        elif P.__z == 0:
            R = Q
        elif Q.__z == 0:
            R = P
        else:
            if P.x != Q.x:
                l = (Q.y - P.y) / (Q.x - P.x)
            elif P.y == Q.y and P.y != 0:
                l = (Fq(3) * P.x * P.x + RPFq.a) / (Fq(2) * P.y)
            else:
                R.set_infinity()
            R.x = l * l - P.x - Q.x
            R.y = (P.x - R.x) * l - P.y
        return R

    def __iadd__(self, P):
        return self + P

    def __neg__(self):
        return RPFq(self.x, Fq(Fq.q - self.y))

    def __rmul__(self, s: int):
        Q = RPFq(0, 0)
        Q.set_infinity()
        T = self
        while s > 0:
            if s & 1 == 1:
                Q += T
            T += T
            s >>= 1
        return Q

    def is_onE(self):
        left = self.y ** 2
        right = self.x ** 3 + RPFq.a * self.x + RPFq.b
        if left == right or self.__z == 0:
            return True
        else:
            return False

    def is_infinity(self):
        if self.__z == 0:
            return True
        else:
            return False

    def print(self):
        if self.__z != 0:
            print('({0}, {1})'.format(self.x, self.y), end='')
        else:
            print("(INFINITY)", end='')

    @staticmethod
    def is_xonE(x):
        y2 = Fq(x ** 3 + RPFq.a * x + RPFq.b)
        if y2.lds() == -1:
            return False
        else:
            return True

    def P_xis(x):
        y2 = x ** 3 + RPFq.a * x + RPFq.b
        y = y2.sqrt()
        return RPFq(x, y)

    def randP():
        while True:
            x = Fq.rand()
            if RPFq.is_xonE(x):
                break
        return RPFq.P_xis(x)

    def printE():
        print('E: y^2 = x^3 + {0}x + {1}'.format(RPFq.a, RPFq.b))
        print('X = {0}'.format(RPFq.X))
        print('q(X) = {0}'.format(Fq.q))
        print('t(X) = {0}'.format(RPFq.t))
        print('r(X) = {0}'.format(RPFq.r))

    def printPs():
        for i in range(Fq.q):
            x = Fq(i)
            if not RPFq.is_xonE(x):
                continue
            else:
                P = RPFq.P_xis(x)
                Q = -P
                if P.y < Q.y:
                    P.print()
                    Q.print()
                elif P.y > Q.y:
                    Q.print()
                    P.print()
                else:
                    P.print()
                print()


