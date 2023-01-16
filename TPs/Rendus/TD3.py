
import time
import timeit
import tp_primes
from matplotlib import pyplot as plt
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
	
	b = ElementDeZnZ(a ** t, n)
	if b == 1:
		return True

	# a**(t*(2**s)) -1
	# ==
	# (a**t - 1) (a**t + 1) ... (a**((2**s) * t) + 1)
	while s > 0 and (b+1) != 0 and (b-1) != 0:
		b = b**2
		s -= 1
	return (b+1) == 0 or (b-1) == 0

def estPremierOuPseudoPremierDansLesBases(n, la):
	""" Teste la pseudo-primalité d'un entier n dans les bases de la
	>>> estPremierOuPseudoPremierDansLesBases(121, [2, 3])
	True
	>>> estPremierOuPseudoPremierDansLesBases(121, [2])
	False
	"""
	for a in la:
		if estPremierOuPseudoPremierDansLaBase(n, a):
			return True
	return False


def lNombresDePoulet(nbits = 16):
	""" Renvoie la liste des nombres de Poulet inférieurs à 2**nbits
	c'est-à-dire pseudopremiers en base 2 voir suite A001567 de l'OEIS
	>>> lNombresDePoulet(10)
	[341, 561, 645]
	"""
	l = []
	for i in range(3, 2**(nbits), 2):
		if estPremierOuPseudoPremierDansLaBase(i, 2) and not estPremier(i):
			l.append(i)
	return l

def estPremier10bits(n):
	if n in [341, 561, 645]:
		return False
	return estPremierOuPseudoPremierDansLaBase(n, 2)

def lBasesDeTestsDePrimalite(nbits = 32, la = tp_primes.p[0:1000], verbose = True):
	""" Renvoie la liste des bases à tester selon
	la valeur du nombre premier à tester :
	à partir de 341, il faut tester avec base 2 et 3
	à partir de 1105, il faut tester avec base 2, 3, 5
	signifiant que 1105 est le premier nombre de faux positif avec 2 et 3

	>>> lBasesDeTestsDePrimalite(11, tp_primes.p[0:5], False)
	[(341, [2, 3]), (1105, [2, 3, 5]), (1729, [2, 3, 5, 7])]
	>>> lBasesDeTestsDePrimalite(10, tp_primes.p[0:5], False)
	[(341, [2, 3])]
	"""
	n = 2 ** nbits
	l = []
	for k in range(3, n, 2):
		if estPremierOuPseudoPremierDansLaBase(k, 2) and not estPremier(k):
			lc = []
			for p in la:
				lc.append(p)
				if estPremierOuPseudoPremierDansLaBase(k, p):
					if verbose:
						print(f"Faux positif avec {p} : ", k)
				else:
					break
			# Append si lc n'est pas déjà présent
			ajout = True
			for _,j in l:
				if (j == lc):
					ajout = False
			if ajout:
				l.append((k, lc))
	return l

if __name__ == "__main__":
	import doctest
	doctest.testmod()

	# Ex 1 : nombre premier de 60 bits, on fait 2^30 tests (calculs jusqu'à la racine carré du nombre)
	# 2^31 == 2 147 483 648				 	: 10^9
	# 2^64 == 18 446 744 073 709 551 616	: 10^19
	
	# Graphique de densité des nombres premiers jusqu'à 1000
	lx = [i for i in range(1000)]
	ly = tp_primes.p[0:1000]
	#print(lx)
	#print(ly)
	plt.plot(lx, ly, '-')
	plt.title("Graphique de densité des nombres premiers")
	plt.show()

	print("estPremierOuPseudoPremierDansLaBase(121, 3) :", estPremierOuPseudoPremierDansLaBase(121, 3))
	print("estPremierOuPseudoPremierDansLaBase(121, 2) :", estPremierOuPseudoPremierDansLaBase(121, 2))

	print("estPremierOuPseudoPremierDansLaBase(341, 2) :", estPremierOuPseudoPremierDansLaBase(341, 2))

	print("lBasesDeTestsDePrimalite(10) :", lBasesDeTestsDePrimalite(10))
	print("lBasesDeTestsDePrimalite(9) :", lBasesDeTestsDePrimalite(9))

	x = lambda: estPremierOuPseudoPremierDansLaBase(121, 3)
	print(f"\nTemps d'éxécution de 1 000 000 éxécutions de estPremierOuPseudoPremierDansLaBase(121, 3) :", round(timeit.timeit(x, number = 1000000), 3), "s")

	n = 18
	t = time.time()
	print(f"\nBases de Tests pour {n} bits :\n",lBasesDeTestsDePrimalite(n, tp_primes.p[0:1000], False))
	print(f"Temps d'éxécution :", round((time.time() - t), 3), "s")


