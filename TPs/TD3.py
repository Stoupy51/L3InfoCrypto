
import timeit
from arithmetiqueDansZ import *

def estPremierOuPseudoPremierDansLaBase(n, a):
	""" Teste la pseudo-primalité d'un entier n en base a
	c'est-à-dire si a**(n-1) == 1[n]
	>>> estPremierOuPseudoPremierDansLaBase(121, 3)
	True
	>>> estPremierOuPseudoPremierDansLaBase(121, 2)
	False
	"""
	if n == 1:
		return False
	if n % 2 == 0:
		return n == 2
	
	# n-1 = t*(2**s)
	# Tant que t est divisible par 2, augmenter s de 1
	t = n - 1
	s = 0
	while t % 2 == 0:
		t //= 2
		s += 1
	
	if (a**t - 1) % n == 0:
		return True

	# a**(t*(2**s)) -1
	# ==
	# (a**t - 1)(a**t + 1)...(a**((2**s) * t) + 1)
	s1 = 0
	while s1 <= s:
		p = t * (2**s1)
		if (a**p + 1) % n == 0:
			return True
		s1 += 1

	return False

def lNombresDePoulet(nbits = 16):
	""" Renvoie la liste des nombres de Poulet inférieurs à 2**nbits
	c'est-à-dire pseudopremiers en base 2 voir suite A001567 de l'OEIS
	>>> lNombresDePoulet(10)
	[341, 561, 645]
	"""
	l = []
	for i in range(3, 2**(nbits//2), 2):
		if estPremierOuPseudoPremierDansLaBase(i, 2) and not estPremier(i):
			l.append(i)
	return l

if __name__ == "__main__":
	import doctest
	doctest.testmod()

	# Ex 1 : nombre premier de 60 bits, on fait 2^30 tests (calculs jusqu'à la racine carré du nombre)
	# 2^31 == 2 147 483 648					: 10^9
	# 2^64 == 18 446 744 073 709 551 616	: 10^19
	
	# Graphique de densité des nombres premiers jusqu'à 1000
	lx = [i for i in range(1000)]
	#ly = [estPremierOuPseudoPremierDansLaBase(i, 2) for i in range(1000)]
	#ly = [isPrime(i) for i in range(1000)]
	#plt.plot(lx, ly, '*')
	#plt.title("Graphique de densité des nombres premiers")
	#plt.show()


	print(estPremierOuPseudoPremierDansLaBase(121, 3))
	print(estPremierOuPseudoPremierDansLaBase(121, 2))
