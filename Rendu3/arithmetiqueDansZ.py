
from copy import copy
from random import randint
from math import sqrt,log
from sympy import isprime

def secondDiviseur(a):
    """Renvoie le premier diviseur de a supérieur à 1
    Ce diviseur est nécessairement premier
    
    >>> secondDiviseur(15845465)
    5
    >>> secondDiviseur(1)==1 and secondDiviseur(2)==2 and secondDiviseur(6)==2
    True
    >>> secondDiviseur(153)==3 and secondDiviseur(157)==157 and secondDiviseur(13)==13
    True
    """
    # Cas a = 1 ou 2
    if a == 1:
        return 1
    if a % 2 == 0:
        return 2
    
    # On teste de 3 jusqu'à la racine carré de a en pas de 2
    for b in range(3, int(sqrt(a)) + 1, 2):
        if a % b == 0:
            return b
    return a


def eDiviseurs(a):
    """renvoie la liste croissante des diviseurs positifs de a

    >>> eDiviseurs(60)
    {1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 60, 30}
    >>> eDiviseurs(1)
    {1}
    >>> eDiviseurs(13)
    {1, 13}
    """
    r = set({1, a})
    
    # Remplissage de l'ensemble
    for b in range(1, int(sqrt(a)) + 1):
        if a % b == 0:
            r.add(b)
            r.add(a // b)
    return r


def lPGCD(a,b):
    """ Renvoie le couple : (liste des dividendes,le PGCD)
    
    >>> lPGCD(360,304)
    ([1, 5, 2], 8)
    >>> lPGCD(517,513)
    ([1, 128], 1)
    >>> lPGCD(513,517)
    ([0, 1, 128], 1)
    """
    lq=[]
    on_n_a_pas_fini=True
    while (on_n_a_pas_fini):
        q,r = a//b , a%b
        if r==0:
            on_n_a_pas_fini=False
        else:
            lq+=[q]
            a,b=b,r
    return lq,b

def lPPCM(a,b):
    """ Renvoie le couple : (liste des dividendes,le PPCM)
    
    >>> lPPCM(360,304)
    ([1, 5, 2], 8)
    >>> lPPCM(517,513)
    ([1, 128], 1)
    >>> lPPCM(513,517)
    ([0, 1, 128], 1)
    """
    lq=[]
    on_n_a_pas_fini=True
    while (on_n_a_pas_fini):
        q,r = a//b , a%b
        if r==0:
            on_n_a_pas_fini=False
        else:
            lq+=[q]
            a,b=b,r
    return lq,b

def PGCD(a,b):
    """
    >>> PGCD(360,304)
    8
    >>> PGCD(517,513)
    1
    >>> PGCD(513,517)
    1

    """
    l,d=lPGCD(a,b)
    return d


def sontPremiers(a,b):
    """
    >>> sontPremiers(10,21) and sontPremiers(100,37) and not(sontPremiers(4,2))
    True

    """
    return PGCD(a,b)==1


def solDiophant(a,b,c):
    """
    Renvoie x et y de Z tels que a.x+b.y=c
    sous la forme x=x0+k.rep' et y=y0+k.b'

    >>> solDiophant(2,5,16) #x0,y0,a',b' et les sols sont x=-32+5.k et y=16-2.k
    (-32, 16, 5, -2)
    >>> x0,y0,cx,cy=solDiophant(13,4,12)
    >>> 13*(x0+1234*cx)+4*(y0+1234*cy)==12
    True
    """
    d=PGCD(PGCD(a,b),c)
    aa,bb,cc=a//d,b//d,c//d
    x0,y0,dd=bezout(aa,bb)# donc a(x-x0)=-b(y-y0)
    assert cc%dd==0," Pas de solutions à l'équation"
    ccc=cc//dd
    return  x0*ccc,y0*ccc,bb,-aa


def bezout(a,b):
    """Renvoie (u,v,d) tel que a.u+b.v=d avec d=PGCD(a,b)
    >>> bezout(360,304)
    (11, -13, 8)
    >>> bezout(1254,493)
    (-149, 379, 1)
    >>> bezout(513,517)
    (129, -128, 1)
    """
    lq,d=lPGCD(a,b)
    u,v=1,-lq[-1]
    for k in range(len(lq)-1):
        u,v=v,u-v*lq[-k-2]
    return u,v,d


def estPremier(n):
    """
    >>> estPremier(13) and estPremier(2) and not(estPremier(6))and not(estPremier(35))
    True
    """
    if n==1 : return False
    if n==2: return True
    if n==3: return True
    if n%2==0: return False
    if n>1E6:return isprime(n) #Pour éviter les ralentissements
    d=3
    rn=int(sqrt(n)+1)
    while n%d!=0 and d<rn:
        d+=2
    return n%d!=0


def nbPremierSuivant(n):
    """Renvoie le plus petit nombre premier strictement supérieur à n
    
    >>> nbPremierSuivant(1)==2 and nbPremierSuivant(3)==5 and nbPremierSuivant(20)==23
    True
    """
    p=n+1
    while not(estPremier(p)):
        p+=1
    return p


def nbPremierEtMoitieSuivant(n):
    """renvoie le couple q,p de nombres premiers avec q=(p-1)/2
    
    >>> nbPremierEtMoitieSuivant(100)
    (107, 53)
    """
    p=nbPremierSuivant(n)
    while not(estPremier((p-1)//2)):
        p=nbPremierSuivant(p+2)
    return p,(p-1)//2


def grandEntier(n):
    """Renvoie le produit de deux nombres premiers choisis au hasard dans [n..2N]"""
    return nbPremierSuivant(randint(n,2*n))*nbPremierSuivant(randint(n,2*n))


def strExp(p):
    """renvoie l'exposant tout beau
    >>> strExp(9)
    '⁹'
    >>> strExp(-19)
    '⁻¹⁹'
    >>> strExp(0)
    '⁰'
    >>> strExp(1)
    ''
    """
    SE="⁰¹²³⁴⁵⁶⁷⁸⁹" #Cela serait malin de créer plutôt un dictionnaire
    SP,SM="⁺","⁻"
    pt=p
    if pt==0:return "⁰"
    if pt==1:return ""
    if pt<0:
        ch=SM
        pt=-pt
    else:
        ch=""
    while pt>0:
        p10p=int(log(pt,10))
        v10=10**p10p
        ch+=SE[pt//v10]
        pt=pt%v10
    return ch


def chFacteursPremiers(n):
    """renvoie une chaine de caractère donnant la
       décomposition en facteurs premiers de n
    
    >>> chFacteursPremiers(120)
    '2³×3×5'
    >>> chFacteursPremiers(3600)
    '2⁴×3²×5²'
    >>> chFacteursPremiers(1)+chFacteursPremiers(2)
    '12'
    >>> chFacteursPremiers(21)
    '3×7'
    """
    l=lFacteursPremiers(n)
    ch=""
    for d,p in l:
        ch+=f"{d}{strExp(p)}×"
    return ch[:-1]


def lFacteursPremiers(n):
    """renvoie une liste donnant la décomposition en facteurs premiers de n
    
    >>> lFacteursPremiers(18)
    [(2, 1), (3, 2)]
    >>> lFacteursPremiers(13)
    [(13, 1)]
    """
    assert isinstance(n,int) and n>0
    if n==1 : return [(1,1)]

    n1=n
    l,d=[],0
    while n1>1:
        dp=secondDiviseur(n1)
        if dp!=d:
            l+=[(dp,1)]
            d=dp
        else:
            l=l[:-1]+[( dp , l[-1][1] +1) ] #On incrémente la puissance
        n1=n1//dp
    return l


def indicatriceEuler(n):
    """
    >>> indicatriceEuler(5)==4 and indicatriceEuler(15)==8 and indicatriceEuler(125)==100
    True
    """
    lfp=lFacteursPremiers(n)
    res=1
    for p,k in lfp:
        res*=(p-1)*p**(k-1)
    return res


def lDecompoPGCDetPPCM(a,b):
    """Renvoie ce couple de décomposition en facteurs premiers
    en utilisant la décomposition en facteurs premier de a et b
    
    #>>> lDecompoPGCDetPPCM(60,700)
    [(2, 2),(5, 1)], [(2, 2), (5, 2), (7, 1)]
    """
    pgcdC, x = lPGCD(a, b)
    ppcmC, x = lPPCM(a, b)
    return [pgcdC,ppcmC]


#Les méthodes magiques : https://blog.finxter.com/python-dunder-methods-cheat-sheet/
class ElementDeZnZ(object):
    "Elément de Z/nZ"
    
    def __init__(self,val,n=256):
        """
        >>> ElementDeZnZ(-1,10)
        ElementDeZnZ(9,10)
        >>> ElementDeZnZ(ElementDeZnZ(9,10))
        ElementDeZnZ(9,10)
        """
        if isinstance(val, ElementDeZnZ):
            self.rep = val.rep
            self.n = val.n
        else:
            self.rep = val % n
            self.n = n


    def __str__(self):
        """
        >>> print(ElementDeZnZ(-1,5))
        4[5]
        """
        return f"{self.rep}[{self.n}]"


    def __repr__(self):
        """
        >>> ElementDeZnZ(-1,5)
        ElementDeZnZ(4,5)
        """
        return f"ElementDeZnZ({self.rep},{self.n})"


    def __add__(self,other):
        """
        >>> ElementDeZnZ(2,10)+ElementDeZnZ(3,10)
        ElementDeZnZ(5,10)
        >>> ElementDeZnZ(2,10)+3
        ElementDeZnZ(5,10)
        """
        if isinstance(other, ElementDeZnZ):        
            return ElementDeZnZ(self.rep + other.rep, self.n)
        else:
            return ElementDeZnZ(self.rep + other, self.n)


    def __radd__(self,other):
        """
        >>> 2+ElementDeZnZ(3,10)
        ElementDeZnZ(5,10)
        """
        return ElementDeZnZ.__add__(self, other)


    def __mul__(self,other):
        """
        >>> ElementDeZnZ(2,10)*ElementDeZnZ(3,10)
        ElementDeZnZ(6,10)
        >>> ElementDeZnZ(2,10)*3
        ElementDeZnZ(6,10)
        """
        if isinstance(other, ElementDeZnZ):
            return ElementDeZnZ(self.rep * other.rep, self.n)
        else:
            return ElementDeZnZ(self.rep * other, self.n)


    def __rmul__(self,other):
        """
        >>> 2*ElementDeZnZ(3,10)
        ElementDeZnZ(6,10)
        """
        return ElementDeZnZ.__mul__(self, other)

    def __div__(self, other):
        return self.__floordiv__(other)

    def __floordiv__(self,other):
        """
        Opération inverse de la multiplication :
        ElementDeZnZ(4,10)//ElementDeZnZ(5,10) doit renvoyer une erreur
        
        >>> ElementDeZnZ(9,10)//ElementDeZnZ(3,10)
        ElementDeZnZ(3,10)
        >>> ElementDeZnZ(1,10)//ElementDeZnZ(3,10)
        ElementDeZnZ(7,10)
        """
        if isinstance(other,ElementDeZnZ):
            b=other.rep
        else:
            b=other
        u,v,d=bezout(b,self.n)
        ch=f"Il n'existe pas de dividende de {b} par {self}"
        assert self.rep %d ==0,ch
        return ElementDeZnZ(u*(self.rep//d),self.n)


    def __eq__(self, other):
        """
        >>> ElementDeZnZ(9,10) == ElementDeZnZ(-1,10)
        True
        >>> ElementDeZnZ(9,10) == ElementDeZnZ(1,10)
        False
        >>> ElementDeZnZ(9,10) == 9
        True
        """
        if isinstance(other, ElementDeZnZ):
            return (self.rep - other.rep) % self.n == 0
        else:
            if not(isinstance(other,int)):
                return False
            else:
                return (self.rep - other) % self.n == 0


    def __neg__(self):
        """
        >>> -ElementDeZnZ(9,10)==ElementDeZnZ(1,10)
        True
        >>> -ElementDeZnZ(9,10)==2
        False
        >>> -ElementDeZnZ(9,10)==1
        True
        """
        return ElementDeZnZ(-self.rep, self.n)


    def __sub__(self,other):
        """
        >>> a4=ElementDeZnZ(-1,5);a1=ElementDeZnZ(1,5);a1+a4==0
        True
        >>> (-a4+a4==0) and (a4//4==1) and (4*a1+(-a1*4)==0)
        True
        """
        return ElementDeZnZ.__add__(self, -other)


    def __rsub__(self,other):
        """
        >>> 4-ElementDeZnZ(3,5)
        ElementDeZnZ(1,5)
        """
        return ElementDeZnZ.__add__(-self, other)


    def __pow__(self, q):
        """ Exponentiation rapide / modulaire
        >>> a=ElementDeZnZ(3,10); a**2==-1 and a**1==3 and a**0==1 and a**3==7 and a**4==1
        True
        """
        # Cas particulier de la puissance négative :
        # on calcule l'inverse et on passe la puissance en positif
        if (q < 0):
            return self.inverse().__pow__(-q)
        
        # Cas général de la puissance positive en exponentiation rapide
        result = 1
        base = self.rep
        power = q
        while power > 0:
            if power % 2 == 1:
                result = (result * base) % self.n
            base = (base * base) % self.n
            power = power // 2
        return ElementDeZnZ(result, self.n)
    
    def __rpow__(self, q):
        """ Exponentiation rapide / modulaire
        >>> 3**ElementDeZnZ(2,10)
        ElementDeZnZ(9,10)
        """
        result = 1
        base = q
        power = self.rep
        while power > 0:
            if power % 2 == 1:
                result = (result * base) % self.n
            base = (base * base) % self.n
            power = power // 2
        return ElementDeZnZ(result, self.n)


    def __int__(self):
        """
        >>> int(ElementDeZnZ(3,10))
        3
        """
        return self.rep
    
    
    def ordre(self):
        """
        Voir http://www.repcrypta.com/telechargements/fichecrypto_107.pdf
        Retourne la puissance à partir de laquelle il est égal
        
        >>> (ElementDeZnZ(2,7)).ordre()
        3
        >>> (ElementDeZnZ(-2,7)).ordre()
        6
        """
        a = self * self.rep
        b = 1
        while (a != self.rep):
            a = a * self.rep
            b += 1
        return b


    def elementPrimitif(self):
        """Renvoie le premier élément primitif (d'ordre n-1) de Z/nZ suivant self
        
        >>> ElementDeZnZ(2,7).elementPrimitif()
        ElementDeZnZ(3,7)
        """
        res=self+1
        while res.ordre()!=self.n-1:
            res=self+1
        return res
    
    
    def estPrimitif(self):
        return self.ordre()==self.n-1
    
    
    def estInversible(self):
        """Il est inversible si son PGCD avec son modulo == 1
        
        >>> ElementDeZnZ(3,5).estInversible()
        True
        >>> ElementDeZnZ(10,12).estInversible()
        False
        """
        return PGCD(self.rep, self.n) == 1
    

    def inverse(self):
        """
        ElementDeZnZ(2,10).inverse() doit renvoyer une erreur
        >>> ElementDeZnZ(3,5).inverse()==2
        True

        """
        u,_,d = bezout(self.rep,self.n)
        assert d == 1,f"{self} n'est pas inversible !"
        #a et n premiers entre eux
        return ElementDeZnZ(u,self.n)     #a.u=1(n)
    
    
    def logDiscret(self,b):
        """Renvoie x tel que ( self.rep**x == b[self.n] )
        n doit être premier pour garantir l'existence
        
        >>> ElementDeZnZ(2,13).logDiscret(8)
        3
        >>> ElementDeZnZ(2,13).logDiscret(3)
        4
        """
        x = 2
        a = self * self.rep
        b = b % self.n
        while (a.rep != b):
            a *= self.rep
            x += 1
        return x


    def valThChinois(self,other):
        """
        Renvoie c(pq) avec a(p) et b(q) tel que x≡a(p) et x≡b(q) <=>x≡c(p.q)$
        >>> ElementDeZnZ(2,7).valThChinois(ElementDeZnZ(3,10))
        ElementDeZnZ(23,70)
        """
        assert PGCD(self.n,other.n)==1,"p et q ne sont pas premiers entre eux"
        u,v,d=bezout(self.n,other.n)
        return ElementDeZnZ( other.rep*self.n*u + self.rep*other.n*v, self.n*other.n)
    
    
    def demoDiv(self):
        for k in range(1,self.n):
            a=ElementDeZnZ(k,self.n)
            try :
                ch=f"{a.rep}×{a.inverse().rep}=1 ({a.n})"
            except :
                ch=f"{a} n'a pas d'inverse"
            try :
                q=(self//a)
                ch+=f" et {a.rep}×{q.rep}={self} "
            except:
                ch+=f" et il n'y a pas de solution à {a.rep}×X={self} "
            print(ch)

    def demo1():
        for k in range(10,12):
            p1,p2,p3 = nbPremierSuivant(4**k),nbPremierSuivant(5**k),nbPremierSuivant(6**k)
            a=ElementDeZnZ(p1,p3)
            print(f"{k:3} : {a.rep}×{a.inverse().rep}=1 ({a.n})")
            print(f"           et {a.rep}{strExp(p2)}={a**p2}")
        
    def estUnCarre(self):
        """ Renvoie True si self est un carré dans ZnZ
        >>> ElementDeZnZ(2,7).estUnCarre()
        True
        >>> ElementDeZnZ(3,7).estUnCarre()
        False
        """
        return (self**((self.n-1)//2)).rep == 1
    
    def racineCarree(self):
        """ Renvoie la racine carrée de self dans ZnZ
        >>> ElementDeZnZ(2,7).racineCarree()
        ElementDeZnZ(4,7)
        """
        assert self.estUnCarre(), (f"{self} n'est pas un carré")
        return self**((self.n+1)//4)

def demoVitesse():
        print("Démo Vitesse")
        print("Factorisation :")
        for p in range(23,26):
                n=grandEntier(2**p)
                print(f"{p}: {n}=={chFacteursPremiers(n)}")

        print("Logarithme discret :")
        for p in range(20,24):
            n=nbPremierSuivant(2**p)
            b=ElementDeZnZ(10**int(p*3/10),n)
            print(f"{p}: 2{strExp(ElementDeZnZ(2,n).logDiscret(b))}=={b}")

ElmtZnZ = ElementDeZnZ

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    #demoVitesse()
    #ElementDeZnZ.demo1()
    #ElementDeZnZ(8,60).demoDiv()

