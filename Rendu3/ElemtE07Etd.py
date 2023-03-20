
from random import *
from math import sqrt
from sympy import isprime
from arithmetiqueDansZ import *
import numpy as np
import matplotlib.pyplot as plt


#Les méthodes magiques : https://blog.finxter.com/python-dunder-methods-cheat-sheet/
#Voir Au coeur du Bitcoin - Programmer la Blockchain ouverte - collection O'Reilly
#Voir https://www.johndcook.com/blog/2018/08/14/bitcoin-elliptic-curves/

class ElemtE07(object):
	"Ensemble des solutions de Y**2 = X**3+7 dans Fp Courbe secp256k1"

	def __init__(self, x, y = "INF", p = 11):
		""" Défini par deux ElemtE07 mais seul le modulo de x est utilisé.
		Celui de y doit être le même que celui de x.
		L'élément neutre est défini par self.y == "INF"

		>>> ElemtE07(ElmtZnZ(7,11),ElmtZnZ(8,11))
		ElemtE07(7,8,11)
		>>> ElemtE07(1,"INF",11)
		ElemtE07(1,"INF",11)
		"""
		# Constructeur par copie
		if (isinstance(x, ElemtE07)):
			self.x = x.x
			self.y = x.y
			self.p = x.p
		else:
			# On copie les paramètres de x si il est un ElmtZnZ
			if (isinstance(x, ElmtZnZ)):
				self.x = x
				if (y == "INF"):
					self.y = y
				else:
					self.y = ElmtZnZ(y, x.n)
				self.p = x.n
			# Sinon on crée des ElmtZnZ à partir des paramètres
			else:
				self.x = ElmtZnZ(x, p)
				if (y == "INF"):
					self.y = y
				else:
					self.y = ElmtZnZ(y, p)
				self.p = p
			
			# On vérifie que p est premier et que l'élément est bien sur la courbe
			assert (isprime(self.p)), (f"P doit être premier (p = {self.p})")
			if (self.y != "INF"):
				assert (self.y**2 == self.x**3 + 7), (f"({self.x}, {self.y}) n'est pas sur E07")


	def lDesElements(p = 47):
		"""
		>>> ElemtE07.lDesElements(5)
		[ElemtE07(0,"INF",5), ElemtE07(2,0,5), ElemtE07(3,2,5), ElemtE07(3,3,5), ElemtE07(4,1,5), ElemtE07(4,4,5)]
		>>> len(ElemtE07.lDesElements(11))
		12
		>>> ElemtE07(6,5,11) in (ElemtE07.lDesElements(11))
		True
		"""
		l = list(ElemtE07.eDesElements(p))
		l.sort(key = lambda x: x.__hash__())
		return l
	

	def eDesElements(p = 47, verbose: bool = False):
		""" Renvoie un ensemble des ElemtE07 de Z/pZ
		>>> ElemtE07.eDesElements(5) == set(ElemtE07.lDesElements(5))
		True
		>>> ElemtE07(8,3,17) in (ElemtE07.eDesElements(17))
		True
		"""
		# On vérifie que p est premier
		assert (isprime(p)), (f"P doit être premier (p = {p})")
		
		# On crée l'ensemble vide et on ajoute les éléments présents sur la courbe
		ensemble = set({})

		# On parcourt tous les éléments possibles
		for x in range(p):
			# Variable temporaire pour éviter de recalculer x**3 + 7
			right = (x**3 + 7) % p

			for y in range(p):
				# Variable temporaire pour éviter de recalculer y**2
				left = (y**2) % p
				# On ajoute l'élément si il est sur la courbe
				if (left == right):
					ensemble.add(ElemtE07(x, y, p))
		
		# On ajoute l'élément neutre
		ensemble.add(ElemtE07(0, "INF", p))
		return ensemble


	def __hash__(self):
		"""On fera une fonction injective afin de l'utiliser également dans binCode"""
		if (self.y == "INF"):
			return (-1 << 64) + self.p
		else:
			return (self.x.rep << 128) + (self.y.rep << 64) + self.p

	def ElemtE07DepuisHash(h):
		""" Renvoie un ElemtE07 à partir d'un hash
		>>> h = ElemtE07(6,5,11).__hash__()
		>>> ElemtE07.ElemtE07DepuisHash(h)
		ElemtE07(6,5,11)
		"""
		p = h & 0xFFFFFFFFFFFFFFFF
		y = (h >> 64) & 0xFFFFFFFFFFFFFFFF
		x = (h >> 128) & 0xFFFFFFFFFFFFFFFF
		if (y == 0xFFFFFFFFFFFFFFFF):
			return ElemtE07(0, "INF", p)
		else:
			return ElemtE07(x, y, p)


	def __str__(self):
		"""
		>>> print(ElemtE07(ElmtZnZ(3,47),ElmtZnZ(9,47)))
		(3,9)[47]
		"""
		if (self.y == "INF"):
			return f"({self.x.rep},\"INF\")[{self.p}]"
		return f"({self.x.rep},{self.y.rep})[{self.p}]"


	def __repr__(self):
		if (self.y == "INF"):
			return f"ElemtE07({self.x.rep},\"INF\",{self.p})"
		else:
			return f"ElemtE07({self.x.rep},{self.y.rep},{self.p})"


	def double(self):
		""" Renvoie le double de l'élément (ce qui est attendu de self + self)
		>>> ElemtE07(2,2,11).double()
		ElemtE07(5,0,11)
		"""
		# Cas de l'élément neutre ou y = 0
		if (self.y == "INF") or (self.y == 0):
			return ElemtE07(0, "INF", self.p)

		# Cas de l'élément A + A
		a = (3 * (self.x**2)) * (2 * self.y).inverse()
		x = a**2 - 2 * self.x
		y = -(a * (x - self.x) + self.y)
		return ElemtE07(x, y, self.p)


	def __add__(self, other):
		""" Renvoie l'addition des deux éléments
		avec les formules d'addition modulo p :
		Cas A + B:
		> a = (yb - ya) / (xb - xa)
		> x = a**2 - xa - xb
		> y = -(a * (x - xa) + ya)

		Cas A + A:
		> a = (3 * (xa**2)) / (2 * ya)
		> x = a**2 - 2 * xa
		> y = -(a * (x - xa) + ya)

		>>> ElemtE07(2,2,11) + ElemtE07(3,1,11)
		ElemtE07(7,3,11)
		>>> (ElemtE07(3,"INF",47) + ElemtE07(3,9,47)) + ElemtE07(3,"INF",47)
		ElemtE07(3,9,47)
		"""
		assert isinstance(other, ElemtE07), (f"other doit être un ElemtE07 (other = {other})")
		assert (self.p == other.p), (f"Les deux éléments doivent être sur le même modulo (self.p = {self.p}, other.p = {other.p})")

		# Cas A + INF ou INF + B
		if (other.y == "INF"):
			return self
		if (self.y == "INF"):
			return other

		if (self.x == other.x):
			# Cas A + -A
			if not(self.y == other.y):
				return ElemtE07(0, "INF", self.p)
			# Cas A + A
			return self.double()
		
		# Cas A + B
		a = (other.y - self.y) * (other.x - self.x).inverse()
		x = a**2 - self.x - other.x
		y = -(a * (x - self.x) + self.y)
		return ElemtE07(x, y, self.p)


	def __mul__(self, k):
		""" Renvoie la multiplication de l'élément par un entier k
		Méthode d'exponentiation rapide pour accélérer le calcul
		
		>>> ElemtE07(6,5,11) * 3
		ElemtE07(5,0,11)
		>>> ElemtE07(15,13,17) * 0
		ElemtE07(0,"INF",17)
		"""
		# Vérification de la validité de k
		assert k >= 0, (f"k doit être positif (k = {k})")

		# Initialisation
		a = self
		total = ElemtE07(0, "INF", self.p)

		# Multiplication rapide
		while (k > 0):
			if (k % 2 == 1):
				total += a
			a = a.double()
			k = k // 2
		return total


	def __rmul__(self, k):
		"""
		>>> 2 * ElmtZnZ(3,10)
		ElmtZnZ(6,10)
		>>> 2 * (ElemtE07(3,"INF",47) + 3*ElemtE07(3,9,47)) + ElemtE07(3,"INF",47)
		ElemtE07(43,32,47)
		"""
		return self.__mul__(k)


	def __eq__(self, other):
		"""
		>>> 3 * ElemtE07(6,5,11) == ElemtE07(5,0,11)
		True
		>>> ElemtE07(0,"INF",47) == 0
		True
		>>> ElemtE07(3,9,47) == ElemtE07(3,"INF",47) or ElemtE07(3,"INF",47) == ElemtE07(3,9,47)
		False
		"""
		if (isinstance(other, int)):
			return self.y == "INF" and other == 0
		else:
			return (self.x == other.x) and (self.y == other.y) and (self.p == other.p)


	def __neg__(self):
		""" Négation de y modulo p
		>>> -ElemtE07(7,3,11)
		ElemtE07(7,8,11)
		"""
		return ElemtE07(self.x, -self.y, self.p)


	def __sub__(self, other):
		"""
		>>> ElemtE07(3,10,11) - ElemtE07(7,3,11)
		ElemtE07(4,7,11)
		>>> ElemtE07(3,9,47) - ElemtE07(3,9,47) == 0
		True
		"""
		return self.__add__(-other)


	def lOrbite(self):
		""" Renvoie la liste des éléments de l'orbite de self sur la courbe (jusqu'à l'élément neutre)
		>>> ElemtE07(2,2,11).lOrbite()
		[ElemtE07(2,2,11), ElemtE07(5,0,11), ElemtE07(2,9,11), ElemtE07(0,"INF",11)]
		"""
		# Initialisation
		l = [self]
		a = self + self

		# Calcul de l'orbite
		while (a != self):
			l.append(a)
			a += self

		return l


	def ordreCourbe(p=17):
		"""
		>>> ElemtE07.ordreCourbe(11)
		12
		"""
		return len(ElemtE07.lDesElements(p))


	def ordrePoint(self):
		"""
		>>> ElemtE07(3,10,11).ordrePoint()
		3
		>>> ElemtE07(7,3,11).ordrePoint()
		12
		"""
		return len(self.lOrbite())


	def estGenerateur(self):
		""" Renvoie True si l'élément est générateur de l'orbite de la courbe
		>>> ElemtE07(7,3,11).estGenerateur()
		True
		>>> ElemtE07(3,10,11).estGenerateur()
		False
		"""
		return ElemtE07.ordreCourbe(self.x.n) == self.ordrePoint()


	def lDesElementsGenerateurs(p=47):
		"""
		>>> ElemtE07.lDesElementsGenerateurs(11)
		[ElemtE07(4,4,11), ElemtE07(4,7,11), ElemtE07(7,3,11), ElemtE07(7,8,11)]
		"""
		return [e for e in ElemtE07.lDesElements(p) if e.estGenerateur()]


	def lDesElementsDOrdrePremier(p=47):
		"""
		>>> ElemtE07.lDesElementsDOrdrePremier(11)
		[ElemtE07(3,1,11), ElemtE07(3,10,11), ElemtE07(5,0,11)]
		"""
		return [e for e in ElemtE07.lDesElements(p) if estPremier(e.ordrePoint())]


	def elemtE07APartirDeX(x:ElmtZnZ):
		"""
		Renvoie un point avec x ou une valeur proche de x comme abscisse
		>>> ElemtE07.elemtE07APartirDeX(ElementDeZnZ(2,11))
		ElemtE07(2,9,11)
		"""
		xx,p=ElmtZnZ(x),x.n
		assert p%2==1
		y2=xx**3+7
		while not(y2.estUnCarre()):  #yy est une racine carré
			xx=xx+1
			y2=xx**3+7
		#print(xx,y2)
		return ElemtE07(xx,y2.racineCarree())


	def randElemtE07(p):
		"""Renvoie un élément non nul au hasard"""
		return ElemtE07.elemtE07APartirDeX(ElmtZnZ(randint(0,p-1),p))


	def randGenerateurE07(p=47):
		"""Renvoie un élément non nul au hasard
		>>> ElemtE07.randGenerateurE07(47).estGenerateur()
		True
		"""
		lel= ElemtE07.lDesElements(p)
		r = choice(lel)
		while not(r.estGenerateur()):
			r = choice(lel)
		return r


	def affichePointMaxDOrdresPremier():
		p=7
		while p<1000:
			p=nbPremierSuivant(p)
			le=ElemtE07.lDesElementsDOrdrePremier(p)
			GMax,omax=None,-1
			for e in le:
				ord=e.ordrePoint()
				if ord>omax:
					GMax,omax=ElemtE07(e),ord
			print(f"Avec F{p} l'ordre premier max est atteint avec {GMax} et vaut : {omax}")


	def afficheGraphique1(p,nbgmax=35):
		#matplotlib.rcParams['text.usetex'] = True # Faire import matplotlib

		plt.grid(True, lw = 1,markevery=1)
		#plt.axis('equal')
		plt.yticks(range(-p,p+1))
		plt.xticks(range(int(-((p*p+7)**1/3)),p+1))
		kmin,kmax=-p,p*p
		if nbgmax>0:
			kmin,kmax=max(-int(sqrt(nbgmax)),-p),min(nbgmax,p**2)
		for k in range(kmin,kmax):
			ly=np.linspace(-p,p,1001)

			lx=[(y**2+k*p-7)**(1/3) if (y**2+k*p-7)>=0 else -(7-y**2-k*p)**(1/3) for y in ly]
			if -2<k<3:
				s=f"Y^2 = X^3-7 {-k:+2}×{p}"
				st=r""
				plt.plot(lx,ly,"-",label=r"$"+s+"$")
			else:
				plt.plot(lx,ly,"-")
		plt.legend(loc='upper right') #Pour afficher les label définis plus haut
		le=ElemtE07.lDesElements(p)
		lx,ly=[],[]
		#print(le)
		for e in le:
			if e!=0:
				lx.append(e.x.rep  )
				ly.append(e.y.rep if e.y.rep<=p//2 else e.y.rep-p)
		print(lx,ly)
		plt.plot(lx,ly,"*r")
		plt.show()


	def demo(p=67,nbgmax=10):
		"""
		Voir https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc

		"""
		le=ElemtE07.lDesElements(p)
		print(f"Liste des {len(le)}  élements des solutions à Y**2==X**3+7 modulo {p} :")
		print(le)
		print(f"Soit {len(le)} éléments")
		print(f"Liste des élements d'ordre Premier : ")
		leop=ElemtE07.lDesElementsDOrdrePremier(p)
		for e in leop:
			print(f"{e}:{e.ordrePoint()}",end="")

		print()
		print(f"Liste des {len(le)}  élements des solutions à Y**2==X**3+7 modulo {p} :")
		print()
		P,Q=le[1],le[2]
		print(f"{P}+{Q}={P+Q}")
		print(f"{P}-{P}==0 : {P-P==0}")

		lop=P.lOrbite()
		print(f"L'orbite de {P=} a {len(lop)} éléments :")
		print(lop)
		#Démo Graphe1
		print(ElemtE07.lDesElements(p))
		ElemtE07.afficheGraphique1(p)
##		for p in [3,5,11,13]:
##			print(ElemtE07.lDesElements(p))
##			ElemtE07.afficheGraphique2(p)


	def afficheClesPourCodage(p=65537,essaiCle=12345):
		x=ElmtZnZ(essaiCle,p)
		M=ElemtE07.elemtE07APartirDeX(x)
		print(M)
		e=ElemtE07.randElemtE07(p)
		print(f"{e=}")
		#el=ElemtE07.eDesElements(p)
		#print(el)
		g=ElemtE07.randGenerateurE07(p)
		print(f"{g=}")


	def demoChiffre(nbBitsCle=32):
		p = nbPremierAleaParNbBits(nbBitsCle*2)
		k = nbPremierAleaParNbBits(nbBitsCle*2)

		le=ElemtE07.lDesElements(p)
		print(f"Liste des {len(le)}  élements des solutions à Y**2==X**3+7 modulo {p} :")
		print(le)
		print(f"Soit {len(le)} éléments")
		print()
		leop=ElemtE07.lDesElementsDOrdrePremier(p)
		for A in leop:
			print(f"{A} a pour ordre premier : {A.ordrePoint()}")



if __name__ == "__main__":
	import doctest
	doctest.testmod()

	p = 11
	ElemtE07.demo(p)



