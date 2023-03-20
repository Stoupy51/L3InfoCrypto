# -*- coding: utf-8 -*-
"""
Codage d'octets
"""
import numpy as np
import matplotlib.pyplot as plt
import random
from arithmetiqueDansZ import *

class fBijOctetsCA(object):
    "Une classe abstraite de bijection de [0..255]"
    def __init__(self ):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __call__(self,octet):
        """Renvoie l'image de octet par la bijection"""
        raise NotImplementedError

    def valInv(self,octetC):
        "Renvoie l'antécédent de octetC"
        raise NotImplementedError

    def construitGraphique(self):
        "f est une fonction bijective de [0..255]"
        lm=[m for m in range(256)]
        lc=[self(m) for m in lm]
        plt.plot(lm,lc,".")
        plt.title(f"{self}")

    def construitGraphiqueDifferentielle(self,df=lambda x:(x+1)%256):
        "df est une fonction bijective appliquant une légère différence de [0..255]"
        lm=[m for m in range(256)]
        lc=[self(m)^self(df(m)) for m in lm]
        plt.plot(lm,lc,".")
        plt.title(f"Diff de {self}")

    def construitGraphiqueLigne(self):
        "f est une fonction bijective de [0..255]"
        lm=[m for m in range(256)]
        lc=[self(m) for m in lm]
        for k in range(256):
            plt.plot([lm[k],lc[k]],[1,0],"-")
        plt.title(f"{self}")

class fAffine(fBijOctetsCA):
     "Une classe abstraite de bijection de [0..255]"
     def __init__(self,a=3,b=7 ):
         assert a%2==1,"a ne doit pas être divisible par 2"
         self.a,self.b=a%256,b%256

     def __repr__(self):
         return f"fAffine({self.a},{self.b})"

     def __call__(self,octet):
         return (octet*self.a+self.b)%256

     def valInv(self,octetC):
         """Renvoie l'antécédent de octetC
         >>> fAffine().valInv(fAffine()(123))
         123
         """
         am1=ElmtZnZ(self.a,256).inverse().rep
         return ((octetC-self.b)*am1)%256

class fMasque(fBijOctetsCA):
     "Une classe abstraite de bijection de [0..255]"
     def __init__(self,oMasque=0b10101010 ):
         self.oMasque=oMasque

     def __repr__(self):
         return f"fMasque({self.oMasque})"

     def __call__(self,octet):
         return octet^self.oMasque

     def valInv(self,octetC):
         """Renvoie l'antécédent de octetC
         >>> fAffine().valInv(fAffine()(123))
         123
         """
         return octetC^self.oMasque



class fPermutationsBits(fBijOctetsCA):
    def __init__(self,lp=[2,4,1,3,6,5,0,7]):
        "Fonction bijective sur [0..255] permutant les bits"
        "par exemple le bit 0 de l'image de arg sera la valeur du bit 2 de arg"
        self.lp=lp
    def __repr__(self):
        return f"fPermutationsBits({self.lp})"

    def __call__(self,octet):
        """
        renvoie l'image de octet
        >>> bin(fPermutationsBits([7,1,2,3,4,5,6,0])(0b11001110))
        '0b1001111'
        >>> bin(fPermutationsBits([1,0,2,3,4,5,6,7])(0b11001110))
        '0b11001101'
        """

        x,lbx,lby = octet , [] , [0]*8

        for k in range(8):
            lbx.append(x%2)
            x=x//2

        lby=[lbx[self.lp[k]] for k in range(8)]

        y=0
        for k in range(7,-1,-1):
            y=2*y+lby[k]
        return y
class fPermut(object):
    """Fonction opérant sur 4bits
    La class contient la liste lp des permutations S4
    >>> [3,2,0,1] in fPermut.lp and len(fPermut.lp)==24
    True
    """
    k,lp=0,[]
    e=set([0,1,2,3])
    l1=list(e)
    for i1 in l1:
         e.discard(i1)
         l2=list(e)
         for i2 in l2:
            e.discard(i2)
            l3=list(e)
            for i3 in l3:
                e.discard(i3)
                i4=e.pop()
                lp.append([i1,i2,i3,i4])
                e.add(i4)
                e.add(i3)
            e.add(i2)
         e.add(i1)

    def f(num,val):
        """Dans le test qui suit on applique la permutation numéro 2 soit [0, 2, 1, 3]
        >>> fPermut.lp[2]
        [0, 2, 1, 3]
        >>> bin(fPermut.f( 2,0b1011))
        '0b1101'
        """
        assert val>=0 and val <16
        lp=fPermut.lp[num]
        lx=[val%2,(val//2)%2,(val//4)%2,(val//8)%2]
        return lx[lp[0]]+2*lx[lp[1]]+4*lx[lp[2]]+8*lx[lp[3]]

class fFeistel(fBijOctetsCA):
     "Voir Introduction à la Cryptographie Dunod chap 5.1"
     def __init__(self,k=123456,r=3 , f = fPermut.f):
         "La fonction f est une fonction  qui à (k,x) associe x crypté avec la clé k"
         self.k,self.r=k,r
         self.f =f

     def __repr__(self):
         return f"fFeistel({self.k=},{self.r=},{self.f=})"

     def __call__(self,octet):
         assert octet>=0 and octet <256
         random.seed(self.k)
         lk=[random.randint(0, 255) %16 for k in range(self.r)]
         l,r=octet//16, octet%16
         for i in range(self.r):
             k=lk[i]
             #print(f"self.f( ({k=},{r=}) )={self.f( (k,r) )}")
             l,r = r , l^self.f( k,r )
             #print(l,r)
         res= r*16+l
         assert res>=0 and res <256
         return res

     def valInv(self,octetC):
         """Renvoie l'antécédent de octetC
         >>> fFeistel().valInv(fFeistel()(7))
         7
         """
         random.seed(self.k)
         lk=[random.randint(0, 255) %16 for k in range(self.r)]
         r,l = octetC//16, octetC%16
         #print(l,r)
         for i in range(self.r-1,-1,-1):#de r-1 à 0 inclu
            k=lk[i]
            #print(f"self.f( ({k=},{l=}) )={self.f( (k,l) )}")

            r,l = l , r^self.f( k,l )
            #print(l,r)
         return l*16+r

def demo():
    for f in [fAffine(),
              fAffine(223,57),
              fMasque(),
              fMasque(0b11101110),
              fPermutationsBits([1,0,2,3,4,5,6,7]),
              fPermutationsBits(),
              fFeistel(),
              fFeistel(134,1),
              fFeistel(134,2),
              fFeistel(134,3),
              fFeistel(134,5),

              fFeistel(134,7),
              fFeistel(134,7,f=lambda k,x:k^x)
              ]:
        plt.subplots_adjust(hspace=0.4) #Pour espacer les graphiques
        plt.title("La fonction {f}")
        plt.subplot(121)
        f.construitGraphique()
        #plt.subplot(223)
        #f.construitGraphiqueLigne()
        plt.subplot(122)
        f.construitGraphiqueDifferentielle()
        plt.show()
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    demo()