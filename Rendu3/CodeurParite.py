
import random
import Colors
from Binaire603 import *
from CodeurCA import *

class CodeurParite(CodeurCA):
	""" Classe définissant un codeur de parité """

	def __init__(self, n:int = 8):

		# Constructeur par copie
		if isinstance(n, CodeurParite):
			self.n = n.n
			self.m_block_size = n.m_block_size

		# Constructeur par valeur
		elif isinstance(n, int):
			self.n = n
			self.m_block_size = (n - 1)**2 # 49 bits si n = 8
		else:
			raise TypeError(f"Erreur : le paramètre passé n'est pas un entier")
		
	def __str__(self):
		return f"Codeur de parité sur {self.n} bits"
	def __repr__(self):
		return f"CodeurParite({self.n})"

	def blocCode(self, M:int, verbose = False) -> int:
		""" Renvoie M codé en parité avec un bit de plus
		>>> print(CodeurParite(8).blocCode(151889728578705))
		9841247361670726809
		"""
		# Vérification de la taille de M (trop grand = erreur)
		if M > (1 << self.m_block_size):
			raise ValueError(f"Erreur : M est trop grand pour être codé en parité : {M} > {self.m_block_size}")

		# Mise en matrice de M pour calculer la parité plus facilement mais pas plus efficacement
		matrice = []
		for i in range(self.n - 1):
			matrice.append([])
			for j in range(self.n - 1):
				matrice[i].append(M & 1)
				M >>= 1

		# On affiche la matrice incomplète si verbose
		if verbose: print(f"Matrice incomplète : {matrice}\n")

		# Calcul de la parité
		matrice.append([])
		for i in range(self.n - 1):
			# On calcule la parité de la ligne
			parite = 0
			for j in range(self.n - 1):
				parite ^= matrice[i][j]
			matrice[i].append(parite)
   
			# On calcule la parité de la colonne
			parite = 0
			for j in range(self.n - 1):
				parite ^= matrice[j][i]
			matrice[-1].append(parite)

		# On calcule la dernière parité
		parite = 0
		for i in range(self.n - 1):
			parite ^= matrice[-1][i]
		matrice[-1].append(parite)

		# On affiche la matrice si verbose
		if verbose: print(f"Matrice complète : {matrice}\n")

		# On remet tout dans un entier
		valc = 0
		for i in range(self.n):
			for j in range(self.n):
				valc <<= 1
				valc += matrice[i][j]
    
		# On renvoie le résultat
		return valc

	def blocDecode(self, valc:int) -> int:
		""" Renvoie M décodé à partir de valc
		>>> c = CodeurParite(8)
		>>> print(c.blocDecode(c.blocCode(5615418648)))
		5615418648
		>>> print(CodeurParite(8).blocDecode(9841247361670726809))
		151889728578705
		"""
		if not self.estBlocValide(valc):
			return self.blocValideLePlusProche(valc)

		# On remet en matrice
		matrice = []
		for i in range(self.n):
			matrice.append([])
			for _ in range(self.n):
				matrice[i].append(valc & 1)
				valc >>= 1
			matrice[i].reverse()
		matrice.reverse()

		# On remet tout dans un entier en ignorant la parité
		r = 0
		for i in range(self.n - 1):
			for j in range(self.n - 1):
				r <<= 1
				r += matrice[self.n - 2 - i][self.n - 2 - j]

		# On renvoie le résultat
		return r
		

	def estBlocValide(self, valc:int, verbose:bool = False) -> bool:
		""" Renvoie True si valc est un bloc valide, False sinon
		On vérifie que la parité est bonne pour chaque ligne et chaque colonne
		"""
		# On remet en matrice
		matrice = []
		for i in range(self.n):
			matrice.append([])
			for _ in range(self.n):
				matrice[i].append(valc & 1)
				valc >>= 1
			matrice[i].reverse()
		matrice.reverse()

		# On vérifie la parité de chaque ligne (et on compare avec la dernière valeur de la ligne)
		estValide = True
		for i in range(self.n):

			# On calcule la parité de la ligne
			parite = 0
			for j in range(self.n - 1):
				parite ^= matrice[i][j]
			
			# On compare avec la dernière valeur de la ligne
			if parite != matrice[i][-1]:
				if verbose: print(f"Erreur de parité sur la ligne {i}")
				estValide = False
		
		# On vérifie la parité de chaque colonne (et on compare avec la dernière valeur de la colonne)
		for j in range(self.n):

			# On calcule la parité de la colonne
			parite = 0
			for i in range(self.n - 1):
				parite ^= matrice[i][j]
			
			# On compare avec la dernière valeur de la colonne
			if parite != matrice[-1][j]:
				if verbose: print(f"Erreur de parité sur la colonne {j}")
				estValide = False

		return estValide
	
	def blocValideLePlusProche(self, valc:int, verbose:bool = False) -> int:
		""" Renvoie le bloc valide le plus proche de valc
		On cherche une erreur de parité sur une ligne et une colonne et on la corrige
		"""
		# On remet en matrice
		matrice = []
		for i in range(self.n):
			matrice.append([])
			for _ in range(self.n):
				matrice[i].append(valc & 1)
				valc >>= 1
			matrice[i].reverse()
		matrice.reverse()

		# On vérifie la parité de chaque ligne (et on compare avec la dernière valeur de la ligne)
		for i in range(self.n):

			# On calcule la parité de la ligne
			parite = 0
			for j in range(self.n - 1):
				parite ^= matrice[i][j]
			
			# On compare avec la dernière valeur de la ligne
			if parite != matrice[i][-1]:
				if verbose: print(f"Erreur de parité sur la ligne {i}")

				# On cherche la colonne qui a une erreur de parité avec la ligne
				for j in range(self.n):
					parite = 0
					for k in range(self.n - 1):
						parite ^= matrice[k][j]
					if parite != matrice[-1][j]:
						if verbose: print(f"Erreur de parité sur la colonne {j}")

						# On corrige l'erreur
						matrice[i][j] ^= 1
						break

		# On remet tout dans un entier en ignorant la parité
		r = 0
		for i in range(self.n - 1):
			for j in range(self.n - 1):
				r <<= 1
				r += matrice[self.n - 2 - i][self.n - 2 - j]

		# On renvoie le résultat
		return r


	def binCode(self, monBinD:Binaire603, verbose = False) -> Binaire603:
		""" Renvoie le Binaire603 codé en parité

		>>> print(CodeurParite(8).binCode(Binaire603("Hey !")).toNumber())
		9512490631043219588
		>>> print(CodeurParite(8).binCode(Binaire603("Heyaaaaaaaaaaaaaaaaaaaaaa !")).toNumber())
		1101470398655224148861438082307466792909387827836669323444163803616017115611106100251647505596563
  		"""
		# Si monBinD est un string, on le convertit en Binaire603
		if isinstance(monBinD, str):
			monBinD = Binaire603(monBinD)

		# Conversion du Binaire603 en entier
		numberD = monBinD.toNumber()
		numberC = 0
		
		# Tant qu'il reste des bits à coder
		while numberD > 0:
			# On calcule le bloc à coder
			bloc = numberD % (1 << self.m_block_size)
			if verbose: print(f"binCode: bloc = {bloc} (en Binaire603 : {Binaire603.fromNumber(bloc)})")

			# On décale number pour les prochains blocs
			numberD >>= (self.n - 1)**2
   
			# On code le bloc et on l'ajoute à numberC
			blocC = self.blocCode(bloc)
			numberC <<= (self.n)**2
			numberC += blocC
			if verbose: print(f"binCode: blocC = {blocC} (en Binaire603 : {Binaire603.fromNumber(blocC)})")

		# On renvoie le résultat
		return Binaire603.fromNumber(numberC)

	def binDecode(self, monBinC:Binaire603, verbose = False) -> Binaire603:
		""" Renvoie le Binaire603 décodé à partir de monBinC
		>>> c = CodeurParite(8)
		>>> print(c.binDecode(c.binCode(Binaire603("Hey !"))).toString())
		Hey !
		>>> c = CodeurParite(8)
		>>> print(c.binDecode(c.binCode(Binaire603("hfurnziufheifezfehjuierhfirhefheifzndfuzhuzdhz !"))).toString())
		hfurnziufheifezfehjuierhfirhefheifzndfuzhuzdhz !
  		"""
		# Si monBinC est un string, on le convertit en Binaire603
		if isinstance(monBinC, str):
			monBinC = Binaire603(monBinC)

		# Conversion du Binaire603 en entier
		numberC = monBinC.toNumber()
		numberD = 0

		# Tant qu'il reste des bits à décoder
		blocMod = (1 << (self.n)**2)
		while numberC > 0:
			# On calcule le bloc à décoder
			blocC = numberC % blocMod
			if verbose: print(f"binDecode: blocC = {blocC} (en Binaire603 : {Binaire603.fromNumber(blocC)})")
   
			# On décale number pour les prochains blocs
			numberC >>= (self.n)**2
   
			# On décode le bloc et on l'ajoute à numberD
			bloc = self.blocDecode(blocC)
			numberD <<= (self.n - 1)**2
			numberD += bloc
			if verbose: print(f"binDecode: bloc = {bloc} (en Binaire603 : {Binaire603.fromNumber(bloc)})")
		
		# On renvoie le résultat
		return Binaire603.fromNumber(numberD)

	def blocAvecErreur(self, valc:int, nbErreurs = 1):
		""" Renvoie le bloc val avec nbErreurs bits changés
		>>> CodeurParite().blocAvecErreur(0, 1) != 0
		True
		"""
		# On remet en matrice
		matrice = []
		for i in range(self.n):
			matrice.append([])
			for _ in range(self.n):
				matrice[i].append(valc & 1)
				valc >>= 1
			matrice[i].reverse()
		matrice.reverse()

		# On ajoute des erreurs
		for _ in range(nbErreurs):
			i = random.randint(0, self.n - 1)
			j = random.randint(0, self.n - 1)
			matrice[i][j] ^= 1
		
		# On remet tout dans un entier en ignorant la parité
		r = 0
		for i in range(self.n - 1):
			for j in range(self.n - 1):
				r <<= 1
				r += matrice[self.n - 2 - i][self.n - 2 - j]

		# On renvoie le résultat
		return r

	
	def demoCorrection():
		""" Fonction de démonstration de la correction d'erreurs """
		print(f"\n\n{Colors.green}Démo de la correction d'erreurs{Colors.reset}")

		# On crée un codeur de parité
		c = CodeurParite(8)

		# On crée un bloc de 32 bits
		bloc = random.randint(0, 2**32 - 1)

		# On code le bloc
		blocCode = c.blocCode(bloc)

		# On ajoute des erreurs
		blocAvecErreurs = c.blocAvecErreur(blocCode, 1)

		# On décode le bloc
		blocDecode = c.blocDecode(blocAvecErreurs)

		# On affiche le résultat
		print(f"Code corrigé ? {Colors.blue}{blocDecode == bloc}{Colors.reset}")
		print(f"bloc = {bloc} (en Binaire603 : {Binaire603.fromNumber(bloc)})")
		print(f"blocDecode = {blocDecode} (en Binaire603 : {Binaire603.fromNumber(blocDecode)})")
		

		

if __name__ == "__main__":
	import doctest
	doctest.testmod()

	# Test du codeur de parité avec 2 à 64 bits
	validite = True
	for i in range(2, 65):
		c = CodeurParite(i)
		texte = Binaire603("Hey !")
		texte2 = Binaire603("Heyaaaaaaaaaaaaaaaaaaaaaa !")
		bool1 = c.binDecode(c.binCode(texte)) == texte
		bool2 = c.binDecode(c.binCode(texte2)) == texte2
		validite = validite and bool1 and bool2
	print(f"Validité: {validite}")
	
	# Test du codeur de parité avec 16 bits
	print("\n\n\nTest avec 16 bits:")
	c = CodeurParite(16)
	texte = Binaire603("Hey !")
	texteC = c.binCode(texte, True)
	texteD = c.binDecode(texteC, True)
	print(f"Validité: [texte: {texteD == texte}]")


	# Test du codeur de parité avec les 1000 premiers caractères de "Les Misérables.txt"
	c = CodeurParite(8)
	file = Binaire603(Binaire603.bin603DepuisFichier("Les Miserables.txt")[0:1000])
	fileC = c.binCode(file, False)
	fileD = c.binDecode(fileC, False)
	print(f"\n\n\nFichier 'Les Miserables.txt':")
	print(f"Fichier de base : {file.toNumber()}")
	print(f"Codé : {fileC.toNumber()}")
	print(f"Décodé : {fileD.toNumber()}")
	print(f"Fichier décodé identique à celui de base : {file == fileD}")

	# Demo de correction d'erreurs
	CodeurParite.demoCorrection()

