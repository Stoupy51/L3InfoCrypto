
import doctest
from random import *
import matplotlib.pyplot as plt

from arithmetiqueDansZ import *

class fBijParDecalage(object):    
    def __init__(self, decal):
        self.decal = ElementDeZnZ(decal, 256)

    def __repr__(self):
        return f"fBijParDecalage({self.decal})"
    
    def __call__(self, octet):
        return (octet + self.decal)
    
    def valInv(self, octet):
        """Renvoie l'antécédent de octet"""
        return (octet - self.decal)

class fBijAffine(object):    
    def __init__(self, a, b):
        self.a = ElementDeZnZ(a, 256)
        self.b = ElementDeZnZ(b, 256)
        self.a_inv = self.a.inverse()

    def __repr__(self):
        return f"fBijAffine({self.a}, {self.b})"
    
    def __call__(self, octet):
        return (self.a * octet + self.b)
    
    def valInv(self, octet):
        """Renvoie l'antécédent de octet"""
        return (self.a_inv * (octet - self.b))

class fFeistel(object):    
    def __init__(self, k = 2, f = fBijParDecalage(37), n = 1):
        self.k = k
        seed(self.k)
        self.lk = [randint(0, 255) for _ in range(n)]
        self.f = f
        self.n = n
    
    def __repr__(self):
        return f"fFeistel({self.k}, {self.f.__repr__()}, {self.n})"
    
    def __call__(self, octet):
        l = octet & 0xF0
        r = octet & 0x0F
        for t in range(self.n):
            l, r = self.lk[t], self.f(r ^ self.lk[t]).rep ^ l
            octet = self.f(r ^ self.k).rep ^ l
        return octet



if __name__ == "__main__":
    doctest.testmod()

    # Par décalage
    f = fBijParDecalage(37)
    lx = [i for i in range(256)]
    ly = [f(i).rep for i in lx]
    plt.plot(lx, ly, '*')
    plt.title(f"Graphique de {f}")
    plt.show()

    # Affine
    f = fBijAffine(5, 10)
    lx = [i for i in range(256)]
    ly = [f(i).rep for i in lx]
    plt.plot(lx, ly, '*')
    plt.title(f"Graphique de {f}")
    plt.show()

    # Feistel
    f = fFeistel(5, f, 1)
    lx = [i for i in range(256)]
    ly = [f(i) for i in lx]
    plt.plot(lx, ly, '*')
    plt.title(f"Graphique de {f}")
    plt.show()



