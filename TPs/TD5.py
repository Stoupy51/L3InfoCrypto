
from random import *
from math import *
from Binaire603 import *
from arithmetiqueDansZ import *
from CodeurCA import *

import matplotlib.pyplot as plt
import numpy as np

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
			mult *= 256
		c = [ 1 for _ in range(self.bits) ]
		p = ElmtZnZ(1, self.bits_int)
		i = 0
		while i < self.bits:
			for byte in monBinD:
				p += ((((byte ** 2 + 7) * 37) << 6) // 47) ^ 887 ^ customSeed
				c[i] = (p.rep * customSeed // 7) % 256
				i += 1
				if i >= self.bits:
					break
		return Binaire603(c)



class hashNaif2(CodeurCA):
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
			mult *= 256
		c = [ 1 for _ in range(self.bits) ]
		i = 0
		paquet1 = ElmtZnZ(7, self.bits_int)
		paquet2 = ElmtZnZ(41, self.bits_int)
		while i < self.bits:
			for byte in monBinD:
				paquet1 = paquet1 * (byte * 7 + (564154587867 ^ paquet2.rep) - customSeed)
				paquet2 = byte * (customSeed - paquet1)
				paquet1, paquet2 = ElmtZnZ(paquet2.rep ^ (customSeed * paquet1.rep), self.bits_int), paquet1
				c[i] = (paquet1.rep // ((paquet2.rep >> 8) + 1) * customSeed // ((61 ^ paquet2.rep) + 1)) % 256
				i += 1
				if i >= self.bits:
					break
		return Binaire603(c)



def testCollision(h, myStr): 
	collisions = 0
	cols = []
	totalTries = 0
	hashStr = h.binCode(myStr)

	for i in range(len(myStr)):
		for j in range(256):
			newStr = myStr[:i] + chr(j) + myStr[i+1:]
			if (newStr != myStr):
				totalTries += 1
				hh = h.binCode(newStr)
				if (hashStr == hh):
					collisions += 1
					cols.append(newStr)

	return collisions, cols, totalTries

def testCollision2(h, myStr, dico, verbose: bool = False): 
	collisions = 0
	cols = []
	hashStr = h.binCode(myStr)
	
	count = 0
	for s in dico:
		if verbose and (count % 50000 == 0):
			print(count, "sur", len(dico))
		count += 1

		hh = h.binCode(s)
		if (hashStr == hh):
			collisions += 1
			cols.append(s)

	return collisions, cols, len(dico)

def testCollisionHasard(myStr, dico): 
	collisions = 0
	cols = []
	hashStr = hash(myStr)
	
	count = 0
	for s in dico:
		if (count % 50000 == 0):
			print(count, "sur", len(dico))
		count += 1

		hh = hash(s)
		if (hashStr == hh):
			collisions += 1
			cols.append(s)

	return collisions, cols, len(dico)


if (__name__ == "__main__"):
	print("Il y a collision :", collision())

	print("\nProbabilité de collision :", calcProbabiltyDebile())
	print("Probabilité de collision :", calcProbability())

	h = hashNaif(32)
	print("\nHash", h.binCode("Bonjour"))
	print("Hash", h.binCode("Bondour"))

	nbits = 4
	texte = "Bonjour"
	h = hashNaif(nbits)
	print(f"\nHash de {texte} : {h.binCode(texte)}")
	nb, cols, totalTries = testCollision(h, texte)
	print(f"Pourcentage de collisions sur {round(100 * nb / totalTries, 5)}% (totalTries = {totalTries})")
	print("Collisions :", cols)

	h = hashNaif2(nbits)
	print(f"\nHash2 de {texte} : {h.binCode(texte)}")
	nb, cols, totalTries = testCollision(h, texte)
	print(f"Pourcentage de collisions sur {round(100 * nb / totalTries, 5)}% (totalTries = {totalTries})")
	print("Collisions :", cols)

	# Chargement du dictionnaire français
	dico = []
	with open("../dico.txt", "r", encoding="utf16") as f:
		lines = f.readlines()
		for line in lines:
			line = line.split(',')[0]
			dico.append(line)
	nbits = 8
	h = hashNaif2(nbits)
	print(f"\nHash2 de {texte} : {h.binCode(texte)}")
	nb, cols, totalTries = testCollision2(h, texte, dico)
	print(f"Pourcentage de collisions sur {round(100 * nb / totalTries, 5)}% (totalTries = {totalTries})")
	print("Collisions :", cols)


	# Test de la probabilité de collision pour hashNaif
	n = 16
	probabilites = []
	for i in range(1, n + 1):
		h = hashNaif(i)
		nb, cols, totalTries = testCollision(h, texte)
		probabilites.append(nb / totalTries)
	lx = np.arange(1, n + 1)
	ly = probabilites
	plt.plot(lx, ly, label = "Probabilité de collision pour hashNaif")
	plt.show()

	# Test de la probabilité de collision pour hashNaif2
	n = 16
	probabilites = []
	for i in range(1, n + 1):
		h = hashNaif2(i)
		nb, cols, totalTries = testCollision(h, texte)
		probabilites.append(nb / totalTries)
	lx = np.arange(1, n + 1)
	ly = probabilites
	plt.plot(lx, ly, label = "Probabilité de collision pour hashNaif2")
	plt.show()

	# Test de la probabilité de collision pour hashNaif2 avec dictionnaire
	n = 16
	probabilites = []
	for i in range(1, n + 1):
		h = hashNaif2(i)
		nb, cols, totalTries = testCollision2(h, texte, dico)
		probabilites.append(nb / totalTries)
	lx = np.arange(1, n + 1)
	ly = probabilites
	plt.plot(lx, ly, label = "Probabilité de collision pour hashNaif2 avec dictionnaire")
	plt.show()

	# Test de la probabilité de collision pour un vrai hasard
	n = 16
	probabilites = []
	for i in range(1, n + 1):
		hh = hash(texte)
		nb, cols, totalTries = testCollisionHasard(texte, dico)
		probabilites.append(nb / totalTries)
	lx = np.arange(1, n + 1)
	ly = probabilites
	plt.plot(lx, ly, label = "Probabilité de collision pour un vrai hasard")
	plt.show()



