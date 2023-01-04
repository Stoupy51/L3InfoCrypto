 # -*- coding: utf-8 -*-
# Créé par Nous

from random import randint
from math import factorial

class Permutation603(object):
    def __init__(self,l=[5,0,1,2,3,4]):
        """permuation de Sn définie par la liste l avec
        l[m]==m' siginifie que m' est l'image de m par cette permuatation
        et on a linv[m']==m
        l ne doit jamais être modifié
        Attention 0 à une image (mais pas n) contrairement à la littérature mathématique"""
        if isinstance(l,Permutation603):
            self.lp= l.lp.copy()
        else:
            self.lp=l.copy() #Pour ne pas faire référence à la même liste
        n=len(self.lp)
        listeOk=True
        for k in range(n):
            if not(k in self.lp):
                listeOk=False
        assert listeOk,"La liste doit définir une permutation sans redite "+str(l)
        self.lpinv=[0]*n
        for k in range(n):
            self.lpinv[self.lp[k]]=k

    def permutAlea(n=6):
        "Renvoie une permutation aléatoire de Sn"
        "Sans utiliser shuffle afin de voir le cardinal de Sn"
        lp=[k for k in range(n)]
        for i in range(n-1):
            j=randint(i+1,n-1)
            lp[i],lp[j]=lp[j],lp[i]
        return Permutation603(lp)
    def permutKieme(k,n=6):
        """Renvoie la kieme permutation de Sn ce qui permet d'associer une clé
        à chaque permutation
        >>> lr=[Permutation603.permutKieme(k,n=3) for k in range(6)]
        >>> le=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,1,0],[2,0,1]]
        >>> sum([1 if Permutation603(l) in lr else 0 for l in le])
        6
        """
        fact=factorial(n)
        assert k>=0 and k<fact
        lValAPrendre=[k for k in range(n)]
        lres=[]
        kr=k
        for i in range(n):
            fact=fact//(n-i)
            ki,kr=kr//fact , kr%fact #Comme pour l'écriture dans une base
            lres.append(lValAPrendre.pop(ki))
        return Permutation603(lres)
    def numPermutation(self):
        """Renvoie le numéro de la permutation
        >>> Permutation603.permutKieme(100,n=5).numPermutation()
        100
        """
        n=len(self)
        fact=factorial(n)
        lValAPrendre=[k for k in range(n)]
        kres=0
        for i in range(n):
            fact=fact//(n-i)
            ki=lValAPrendre.index(self.lp[i])
            lValAPrendre.pop(ki)
            kres+=ki*fact

        return kres
    def __len__(self):
        return len(self.lp)

    def __str__(self):
        s="("
        for x in self.lp:
            s=s+str(x)+","
        return s[:-1]+")"

    def __repr__(self):
        return f"Permutation603({self.lp})"

    def __mul__(self,other):
        """
        >>> Permutation603([1,2,0])*Permutation603([2,0,1])
        Permutation603([0, 1, 2])
        >>> Permutation603([1,2,0])*[2,0,1]
        Permutation603([0, 1, 2])
        """
        assert len(self)==len(other)
        if isinstance(other,Permutation603):
            lother=other.lp
        else:
            lother=other

        ll=[self.lp[lother[k]] for k in range(len(self))]
        return Permutation603(ll)

    def ordre(self):
        """Renvoie l'ordre de la permutation
        >>> Permutation603([1,2,3,0]).ordre()
        4
        >>> Permutation603([1,0,2,3]).ordre()
        2
        """
        p=self
        q=p*p
        k=2
        while q!=p:
            q=q*p
            k=k+1
        return k-1


    def __pow__(self, n):
        """
        >>> Permutation603([1,2,3,0])**2
        Permutation603([2, 3, 0, 1])
        >>> Permutation603([1, 2, 3, 0])**4
        Permutation603([0, 1, 2, 3])
        >>> Permutation603([1, 2, 3, 0])**(-1)
        Permutation603([3, 0, 1, 2])

        """
        if n==1:
            res= Permutation603(self)
        elif n==0:
            res= Permutation603([k for k in range(self.taille)])
        elif n<0:
            res=  (Permutation603(self.lpinv))**(-n)
        elif n%2==0:
            res=  (self*self)**(n//2)
        else:
            res=  (self)**(n-1)*self
        return res

    def __rmul__(self, other):
        return Permutation603(other)*self

    def __eq__(self,other):
        """
        >>> Permutation603([1,2,0])== [1,2,0]
        True
        >>> Permutation603([1,2,0])==Permutation603([1,0,2])
        False
        """
        if isinstance(other,Permutation603):
            res = self.lp==other.lp
        else:
            res = self.lp== other
        return res

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(Permutation603.permutAlea(256))


    p=Permutation603.permutKieme(100,n=5)
    print(p.numPermutation())

