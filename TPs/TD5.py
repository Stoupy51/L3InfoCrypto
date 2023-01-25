
from random import *
from math import *
from Binaire603 import *
from arithmetiqueDansZ import *
from CodeurCA import *

def collision(n = 60, N = 365):
	e = set({})
	for i in range(1, n+1):
		e.add(randint(1, N))
		if len(e) < i:
			return True
	return False

def calcProbabiltyDebile(n = 60, N = 365, tours = 10000):
	collisions = 0
	for i in range(tours):
		if collision(n, N):
			collisions += 1
	return collisions / tours

def calcProbability(n = 60, N = 365):
	return 1 - (1 - 1/N)**(n*(n-1)/2)




class hashNaif(CodeurCA):
	""" Hashage naif """

	def __init__(self, bits = 32):
		if (isinstance(bits, hashNaif)):
			self.bits = bits.bits
			self.bits_int = bits.bits_int
		else:
			self.bits = bits
			self.bits_int = 2 ** bits
	
	def binCode(self, monBinD: Binaire603) -> Binaire603:
		if not(isinstance(monBinD, Binaire603)):
			monBinD = Binaire603(monBinD)
		customSeed = 1
		mult = 1
		for b in monBinD:
			customSeed += b * mult
			mult *= 2
		c = [ 1 for _ in range(self.bits) ]
		p = ElementDeZnZ(1, self.bits_int)
		i = 0
		while i < self.bits:
			for byte in monBinD:
				if i >= self.bits:
					break
				for _ in range(77):
					p += (byte ** 2 + 7) * 37 << 6 // 47
				c.append((p.rep * customSeed // 7) % 256)
				i += 1
		return Binaire603(c)

def testCollision(myStr, nbits = 16):
	h = hashNaif(nbits)
	collisions = 0
	dH = dict()

	for i in range(len(myStr)):
		for j in range(256):
			newStr = myStr[:i] + chr(j) + myStr[i+1:]
			hh = h.binCode(newStr)
			if hh in dH:
				collisions += 1
				print(newStr, dH[hh])
			else:
				dH[hh] = newStr

	return collisions


if (__name__ == "__main__"):
	print("Il y a collision :", collision())

	print("\nProbabilité de collision :", calcProbabiltyDebile())
	print("Probabilité de collision :", calcProbability())

	h = hashNaif(32)
	print("\nHash", h.binCode("Bonjour"))
	print("Hash", h.binCode("Bondour"))

	print("\nCollision :", testCollision("Hey"))

