
from arithmetiqueDansZ import *
import matplotlib.pyplot as plt
from random import *
import random

class fBijOctetsCA(object) :
    "Une classe abstraite de bijective de [0..255]"
    def __init__ (self ) :
        raise NotImplementedError

    def __repr__ (self ) :
        raise NotImplementedError

    def __call__ (self ) :
        """Renvoie  l'image de octet par la bijection"""
        raise NotImplementedError

    def valInv(self, octetC) :
        """Renvoie l'antécédent de octetC"""
        raise NotImplementedError

class fBijParDecalage(fBijOctetsCA) :

    def __init__(self,decalage) :
        self.decalage = ElementDeZnZ(decalage,256)

    def __repr__(self) :
        return f"fBijParDecalage({self.decalage})"

    def __str__(self) :
        return f"fBijParDecalage({self.decalage})"

    def __call__(self,octet) :
        return self.decalage + octet

    def valInv(self, octetc) :
        return octetC - self.decalage

class fBijAffine(fBijOctetsCA) :

    def __init__(self,a,b) :
        self.a = ElementDeZnZ(a,256)
        self.b = ElementDeZnZ(b,256)
        self.a_inv = self.a.inverse()

    def __repr__(self) :
        return f"fBijAffine({self.a}, {self.b})"

    def __str__(self) :
        return f"fBijAffine({self.a}, {self.b})"

    def __call__(self,octet) :
        return (self.a * octet + self.b)

    def valInv(self, octet) :
        return (self.a_inv * (octet - self.b))

class fBijFeistel(fBijOctetsCA):
    "Voir Introduction à la Cryptographie Dunod chap 5.1"
    def __init__(self,k=123456,r=3 , f = fBijParDecalage(55) ):
        self.r = r
        self.k = k
        self.f = f

    def __repr__(self):
        return f"fBijFeistel({self.k},{self.r},{self.f})"

    def __call__(self,octet):
        assert octet>=0 and octet <256
        random.seed(self.k)
        print("self.r : ",self.r)
        print([random.randint(0, 255) %16 for k in range(self.r)])
        lk=[random.randint(0, 255) %16 for k in range(self.r)]
        l = octet // 16
        r = octet % 16

        print(l,r)
        for i in range(self.r):
            k=lk[i]
            #print(f"self.f( ({k=},{r=}) )={self.f( (k,r) )}")
            l,r = r , l^self.f( k,r )
            #print(l,r)
        res= r*16+l
        assert res>=0 and res <256
        return res

    def valInv(self,octetC):
        random.seed(self.k)
        lk=[random.randint(0, 255) %16 for k in range(self.r)]

        r = octetC // 16
        l = octetC % 16
        #print(l,r)
        for i in range(self.r-1,-1,-1):#de r-1 à 0 inclu
            k=lk[i]
            #print(f"self.f( ({k=},{l=}) )={self.f( (k,l) )}")

            r,l = l , r^self.f( k,l )
            #print(l,r)
        return l*16+r

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    #Bij par Affine
    f = fBijAffine(5,10)
    lx = [i for i in range(256)]
    ly = [f(i).rep for i in lx]
    plt.plot(lx, ly, '*')
    plt.title(f"Graphique de {f.__repr__()}")
    plt.show()

    #Bij par Feistel
    f = fBijFeistel(5, f, 1)
    lx = [i for i in range(256)]
    ly = [f(i) for i in lx]
    plt.plot(lx, ly, '*')
    plt.title(f"Graphique de {f}")
    plt.show()
    
