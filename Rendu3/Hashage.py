
from random import *
from math import *
from Binaire603 import *
from arithmetiqueDansZ import *
from CodeurCA import *

import Colors
import matplotlib.pyplot as plt
import numpy as np

def collision(n = 60, N = 365):
	""" Renvoie True si il y a collision dans un groupe de N personnes pour n personnes, False sinon
	Dans cet exemple, la probabilité de collision est un peu plus de 0.99
	>>> collision(60, 365)
	True
	"""
	e = set({})
	for i in range(1, n+1):
		e.add(randint(1, N))
		if len(e) < i:
			return True
	return False

def calcProbabiltyDebile(n = 60, N = 365, tours = 10000):
	""" Calcule la probabilité de collision pour n personnes dans un groupe de N personnes"""
	collisions = 0
	for _ in range(tours):
		if collision(n, N):
			collisions += 1
	return collisions / tours

def calcProbability(n = 60, N = 365):
	""" Calcule la probabilité de collision pour n personnes dans un groupe de N personnes en utilisant une formule mathématique"""
	return 1 - (1 - 1/N)**(n*(n-1)/2)




class hashNaif(CodeurCA):
	""" Hashage naif (premier test avec tentative de trucs bizarres) """

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
	""" Hashage naif 2 (Deuxième test) """

	def __init__(self, bits = 32):
		if (isinstance(bits, hashNaif)):
			self.bits = bits.bits
		else:
			self.bits = bits
	
	def binCode(self, monBinD: Binaire603) -> Binaire603:
		"""
		Le hashage fonctionne de la manière suivante :
		- On calcule une "seed" à partir de la chaîne de caractères à hasher
		- On initialise un tableau de bits à 1 (c: notre future hash)
		- On initialise une variable paquet1 à 13841 et une variable paquet2 à 61231 (modulo 2^bits)
		- On parcourt la chaîne de caractères à hasher (pour chaque bit du tableau de bits) :
			- On multiplie paquet1 par (byte * 7 + (564154587867 ^ paquet2) - seed)
			- On multiplie paquet2 par (byte * (seed - paquet1))
			- On inverse paquet1 et paquet2 tout en application une formule "magique" à paquet1
			- On ajoute le résultat de la multiplication de paquet1 et paquet2 modulo 2^bits au tableau de bits

		( J'ai fait des modifications, mais je ne sais plus lesquelles, donc je laisse le code d'origine en commentaire )

		@return c (Binaire603) : Le hashage de la chaîne de caractères

		>>> print(hashNaif2(32).binCode("Bonjour"))

		"""
		# Conversion de la chaîne de caractères en Binaire603 si ce n'est pas déjà le cas
		if not(isinstance(monBinD, Binaire603)):
			monBinD = Binaire603(monBinD)

		# Calcul de la seed en appliquant une formule spéciale et en remplaçant tous les espaces
		customSeed = monBinD.toNumber()
		highValue = 2 ** (self.bits * 2)
		mediumValue = 2 ** self.bits

		# On applique une formule magique à la seed pour éviter d'avoir la même pour la même chaîne de caractères sur différents bits
		customSeed = (customSeed * monBinD.toNumber() + self.bits * 91) % mediumValue

		# Initialisation du tableau de bits et des variables paquet1 et paquet2
		c = [ 1 for _ in range(self.bits) ]
		paquet1 = ElmtZnZ(13841, highValue)
		paquet2 = ElmtZnZ(61231, highValue)

		# Parcours de la chaîne de caractères à hasher (pour chaque bit du tableau de bits)
		i = 0
		while i < self.bits:
			for byte in monBinD:
				# Formules magiques
				paquet1 = paquet1 - ((byte + self.bits + i + 1) * 7 - (564157867 ^ paquet2.rep) - customSeed) + 1
				paquet2 = (byte - 89 * self.bits + i + 1) * (customSeed - paquet1) + 1

				# Inversion de paquet1 et paquet2 tout en application d'une formule magique à paquet1
				paquet1, paquet2 = ElmtZnZ(paquet2.rep ^ (customSeed * paquet1.rep), highValue) + 1, paquet1 + 1

				# Ajout du résultat de la multiplication de paquet1 et paquet2 modulo 2^bits au tableau de bits
				# tout en appliquant une autre formule magique à ce résultat le tout modulo 256
				c[i] = (c[i] + customSeed + i + (paquet1.rep // ((paquet2.rep >> 8) + 1) + customSeed // ((61 ^ paquet2.rep) + 1)) + 1) % 256
			
			# On passe au bit suivant
			i += 1
		return Binaire603(c)

class hashDaviesMeyer(CodeurCA):
	""" Hashage de Davies-Meyer """
	def __init__(self, bits = 32):
		if (isinstance(bits, hashDaviesMeyer)):
			self.bits = bits.bits
			self.bits_int = bits.bits_int
		else:
			self.bits = bits
			self.bits_int = 2 ** bits
	
	def binCode(self, monBinD: Binaire603 | str) -> Binaire603:
		""" Hashage de Davies-Meyer
		@param monBinD : La chaîne de caractères à hasher
		@return c (Binaire603) : Le hashage de la chaîne de caractères
		"""
		# Conversion de la chaîne de caractères en Binaire603 si ce n'est pas déjà le cas
		if (isinstance(monBinD, str)):
			monBinD = Binaire603(monBinD)
		
		# Initialisation du tableau de bits
		c = [ 1 for _ in range(self.bits) ]
		
		raise NotImplementedError("Pas encore implémenté")



def testCollision(h, myStr): 
	""" Teste si une collision est possible pour une chaîne de caractères donnée en
	comparant la chaîne de caractères avec toutes les petites dérives possibles de celle-ci

	@param h : L'objet hash à utiliser
	@param myStr : La chaîne de caractères à tester

	@return collisions : Le nombre de collisions trouvées
	@return cols : La liste des collisions trouvées
	@return totalTries : Le nombre de tentatives effectuées
	"""
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
	""" Teste si une collision est possible pour une chaîne de caractères donnée en
	comparant la chaîne de caractères avec toutes les chaînes de caractères d'un dictionnaire

	@param h : L'objet hash à utiliser
	@param myStr : La chaîne de caractères à tester
	@param dico : Le dictionnaire à utiliser
	@param verbose : Affiche des informations sur l'avancement du test

	@return collisions : Le nombre de collisions trouvées
	@return cols : La liste des collisions trouvées
	@return totalTries : Le nombre de tentatives effectuées
	"""
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

def testCollisionHasard(myStr, dico, verbose: bool = False):
	""" Tente de tester si une collision est possible pour une chaîne de caractères donnée en
	comparant la chaîne de caractères avec toutes les chaînes de caractères hashées d'un dictionnaire

	@param myStr : La chaîne de caractères à tester
	@param dico : Le dictionnaire à utiliser

	@return collisions : Le nombre de collisions trouvées
	@return cols : La liste des collisions trouvées
	@return totalTries : Le nombre de tentatives effectuées
	"""
	collisions = 0
	cols = []
	hashStr = hash(myStr)
	
	count = 0
	for s in dico:
		if verbose and (count % 50000 == 0):
			print(count, "sur", len(dico))
		count += 1

		hh = hash(s)
		if (hashStr == hh):
			collisions += 1
			cols.append(s)

	return collisions, cols, len(dico)






















if (__name__ == "__main__"):
	texte = "Bonjour à toutes et à tous !!!"
	fauxTexte = "Bondour à toutes et à tous !!!"

	# Jeu des naissances
	print(f"\n{Colors.green}Jeu des naissances{Colors.reset}")
	print("il y a collision :", collision())
	print("Probabilité de collision :", calcProbabiltyDebile())
	print("Probabilité de collision :", calcProbability())

	# Test de hash naif
	h = hashNaif(32)
	print(f"\n{Colors.green}Test de hash naif 1{Colors.reset}")
	print(f"Hash de '{texte}' sur", h.binCode(texte))
	print(f"Hash de '{fauxTexte}' sur", h.binCode(fauxTexte))

	# Test des collisions sur hash naif
	print(f"\n{Colors.green}Test des collisions sur hash naif 1 pour '{texte}'{Colors.reset}")
	nbits = 4
	h = hashNaif(nbits)
	print(f"Hash de {texte} : {h.binCode(texte)}")
	nb, cols, totalTries = testCollision(h, texte)
	print(f"Pourcentage de collisions sur {round(100 * nb / totalTries, 5)}% (totalTries = {totalTries})")
	print("Collisions :", cols)

	# Test de hash naif 2
	h = hashNaif2(32)
	print(f"\n{Colors.green}Test de hash naif 2{Colors.reset}")
	print(f"Hash de '{texte}' sur", h.binCode(texte))
	print(f"Hash de '{fauxTexte}' sur", h.binCode(fauxTexte))

	# Test des collisions sur hash naif 2
	print(f"\n{Colors.green}Test des collisions sur hash naif 2{Colors.reset}")
	h = hashNaif2(nbits)
	print(f"Hash de {texte} : {h.binCode(texte)}")
	nb, cols, totalTries = testCollision(h, texte)
	print(f"Pourcentage de collisions sur {round(100 * nb / totalTries, 5)}% (totalTries = {totalTries})")
	print("Collisions :", cols)

	# Chargement du dictionnaire français (une partie car trop long sinon)
	print(f"\n{Colors.green}Chargement du dictionnaire français pour tester hashNaif2{Colors.reset}")
	dico = []
	with open("../dico.txt", "r", encoding="utf16") as f:
		lines = f.readlines()
		for line in lines:
			line = line.split(',')[0]
			dico.append(line)
	nbits = 8
	h = hashNaif2(nbits)
	print(f"Hash2 de {texte} : {h.binCode(texte)}")
	nb, cols, totalTries = testCollision2(h, texte, dico)
	print(f"Pourcentage de collisions sur {round(100 * nb / totalTries, 5)}% (totalTries = {totalTries})")
	print("Collisions :", cols)

















	# Test de la probabilité de collision pour hashNaif
	print(f"\n\n{Colors.green}Test de la probabilité de collision pour hashNaif1{Colors.reset}")
	n = 16
	probabilites = []
	for i in range(1, n + 1):
		h = hashNaif(i)
		nb, cols, totalTries = testCollision(h, texte)
		probabilites.append(nb / totalTries)
	lx = np.arange(1, n + 1)
	ly = probabilites
	plt.plot(lx, ly)
	plt.title("Probabilité de collision pour hashNaif1 en fonction du nombre de bits")
	plt.show()

	# Test de la probabilité de collision pour hashNaif2
	print(f"\n{Colors.green}Test de la probabilité de collision pour hashNaif2{Colors.reset}")
	n = 16
	probabilites = []
	for i in range(1, n + 1):
		print(f"Test pour {i} bits...")
		h = hashNaif2(i)
		nb, cols, totalTries = testCollision(h, texte)
		probabilites.append(nb / totalTries)
	lx = np.arange(1, n + 1)
	ly = probabilites
	plt.plot(lx, ly)
	plt.title("Probabilité de collision pour hashNaif2 en fonction du nombre de bits")
	plt.show()

	# Test de la probabilité de collision pour hashNaif2 avec dictionnaire
	print(f"\n{Colors.green}Test de la probabilité de collision pour hashNaif2 avec dictionnaire{Colors.reset}")
	n = 16
	probabilites = []
	for i in range(1, n + 1):
		print(f"Test pour {i} bits...")
		h = hashNaif2(i)
		nb, cols, totalTries = testCollision2(h, texte, dico)
		probabilites.append(nb / totalTries)
	lx = np.arange(1, n + 1)
	ly = probabilites
	plt.plot(lx, ly)
	plt.title("Probabilité de collision pour hashNaif2 avec dictionnaire en fonction du nombre de bits")
	plt.show()

	# Test de la probabilité de collision pour un vrai hasard
	print(f"\n{Colors.green}Test de la probabilité de collision pour un vrai hasard{Colors.reset}")
	n = 16
	probabilites = []
	for i in range(1, n + 1):
		print(f"Test pour {i} bits...")
		hh = hash(texte)
		nb, cols, totalTries = testCollisionHasard(texte, dico)
		probabilites.append(nb / totalTries)
	lx = np.arange(1, n + 1)
	ly = probabilites
	plt.plot(lx, ly)
	plt.title("Probabilité de collision pour un vrai hasard en fonction du nombre de bits")
	plt.show()



