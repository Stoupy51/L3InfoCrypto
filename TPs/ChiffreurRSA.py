
import timeit
import tp_primes
from random import randint
from arithmetiqueDansZ import *
from Binaire603 import Binaire603

from CodeurCA import CodeurCA

class ChiffreurRSA(CodeurCA):
	""""""
	def __init__(self, e = 7, d = 23, n = 55):
		if isinstance(e, ChiffreurRSA):
			self.e = e.e
			self.d = e.d
			self.n = e.n
		else:
			self.e = ElementDeZnZ(e, n)
			self.d = ElementDeZnZ(d, n)
			self.n = n
	
	def generateKeys():
		#p = tp_primes.p[randint(0, tp_primes.pLen-1)]
		p = tp_primes.p[randint(0, 10)]
		q = p
		while (p == q):
			#q = tp_primes.p[randint(0, tp_primes.pLen-1)]
			q = tp_primes.p[randint(0, 10)]
		n = p * q
		phi = (p - 1) * (q - 1)
		e = p
		while (e == p or e == q or sontPremiers(e, phi) != 1):
			#e = tp_primes.p[randint(0, tp_primes.pLen-1)]
			e = tp_primes.p[randint(0, 10)]
		d = ElementDeZnZ(e, phi).inverse().rep
		#print(f"p = {p}, q = {q}, n = {n}, phi = {phi}, e = {e}, d = {d}")
		return (e, d, n)

	def __str__(self):
		return f"ChiffreurRSA avec e = {self.e}, d = {self.d} et n = {self.n}"
	def __repr__(self):
		return f"ChiffreurRSA({self.e=}, {self.d=}, {self.n=})"

	def binCode(self, monBinD:Binaire603) -> list:
		""" Chiffre un message binaire en utilisant la clé publique
		#>>> ChiffreurRSA().binCode(Binaire603("Bonjour"))
		Binaire603([ 0x0a, 0x0a, 0x0a, 0x0a, 0x0a])
		"""
		return [ (b ** self.e).rep for b in monBinD ]
	
	def __call__(self, monBinD:Binaire603) -> list:
		return self.binCode(monBinD)

	def binDecode(self, monBinC:list) -> Binaire603:
		return Binaire603([ (b ** self.d).rep for b in monBinC ])


if __name__ == "__main__":
	import doctest
	doctest.testmod()
	x = lambda: ChiffreurRSA.generateKeys()
	print(f"Temps d'éxécution :", round(timeit.timeit(x, number = 100), 3), "s")
	print(ChiffreurRSA.generateKeys())
	
	f = ChiffreurRSA()
	texte = "Bonjour"
	c = f(Binaire603(texte))
	d = f.binDecode(c)
	print(f)
	print("Texte :", texte)
	print("Chiffré :", c)
	print("Déchiffré :", d.toString())

