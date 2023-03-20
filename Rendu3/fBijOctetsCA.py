
from random import *
from bijectionDOctets import *
import matplotlib.pyplot as plt

from arithmetiqueDansZ import *

class fPermutationsBits(fBijOctetsCA):
	def __init__(self,lp=[2,4,1,3,6,5,0,7]):
		self.lp=lp

	def __repr__(self):
		return f"fPermutationsBits({self.lp})"

	def __call__(self,octet):
		""" Renvoie l'image de octet
		>>> bin(fPermutationsBits([7,1,2,3,4,5,6,0])(0b11001110))
		'0b1001111'
		>>> bin(fPermutationsBits([1,0,2,3,4,5,6,7])(0b11001110))
		'0b11001101'
		"""
		x, y, lbx, lby = octet, 0, [], [0]*8
		for k in range(8):
			lbx.append(x%2)
			x=x//2
		lby = [lbx[self.lp[k]] for k in range(8)]
		for k in range(7,-1,-1):
			y = 2 * y + lby[k]
		return y

class fBijParDecalage(object):    
	def __init__(self, decal):
		self.decal = ElmtZnZ(decal, 256)

	def __repr__(self):
		return f"fBijParDecalage({self.decal})"
	
	def __call__(self, octet):
		return (octet + self.decal)
	
	def valInv(self, octet):
		"""Renvoie l'antécédent de octet"""
		return (octet - self.decal)

class fBijAffine(object):    
	def __init__(self, a, b):
		self.a = ElmtZnZ(a, 256)
		self.b = ElmtZnZ(b, 256)
		self.a_inv = self.a.inverse()

	def __repr__(self):
		return f"fBijAffine({self.a}, {self.b})"
	
	def __call__(self, octet):
		return (self.a * octet + self.b)
	
	def valInv(self, octet):
		""" Renvoie l'antécédent de octet """
		return (self.a_inv * (octet - self.b))

class fFeistel(object):    
	def __init__(self, k = 2, f = fPermut.f, n = 1):
		self.k = k
		self.f = f
		self.n = n
		# On initialise la liste des clés avec des valeurs aléatoires basées sur la seed k
		seed(k)
		self.lk = [randint(0, 15) for _ in range(n)]

	def __repr__(self):
		return f"fFeistel({self.k}, {self.f.__repr__()}, {self.n})"

	def __call__(self, octet):
		# On sépare l'octet en deux parties de 4 bits
		left = (octet & 0xF0) >> 4
		right = octet & 0x0F

		# On applique la fonction f n fois en alternant les parties gauche et droite
		for i in range(self.n):
			left, right = right, left ^ self.f(self.lk[i], right)
		
		# On recombine les deux parties
		return (left << 4) ^ right

	def valInv(self, octet):
		""" Fonction inverse de __call__
		>>> fFeistel().valInv(fFeistel()(51))
		51
		"""
		# On sépare l'octet en deux parties de 4 bits
		left = (octet & 0xF0) >> 4
		right = octet & 0x0F

		# On applique la fonction f n fois en alternant les parties gauche et droite (en sens inverse)
		for i in range(self.n-1, -1, -1):
			right, left = left, right ^ self.f(self.lk[i], left)
		
		# On recombine les deux parties
		return (left << 4) ^ right



if __name__ == "__main__":
	import doctest
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
	for c in range(1,8):
		f = fFeistel(5, fPermut.f, c)
		lx = [i for i in range(256)]
		ly = [f(i) for i in lx]
		plt.plot(lx, ly, '*')
		plt.title(f"Graphique de {f}")
		plt.show()


