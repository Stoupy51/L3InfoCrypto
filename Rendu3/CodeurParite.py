
from Binaire603 import *
from CodeurCA import *

class CodeurParite(CodeurCA):
	""" Classe définissant un codeur de parité """
	def __init__(self, n:int):
		# Constructeur par copie
		if isinstance(n, CodeurParite):
			self.n = n.n
			self.m_block_size = n.m_block_size
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
		"""
		if not self.estBlocValide(valc):
			return self.blocValideLePlusProche(self, valc)

		# On remet en matrice
		matrice = []
		for i in range(self.n):
			matrice.append([])
			for j in range(self.n):
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
		

	def estBlocValide(self, valc:int) -> bool:
		""" Renvoie True si valc est un bloc valide, False sinon """
		return True

	def binCode(self, monBinD:Binaire603, verbose = False) -> Binaire603:
		""" Renvoie le Binaire603 codé en parité
		>>> c = CodeurParite(8)
		>>> print(c.binCode(Binaire603("Hey !")).toNumber())
		9512490631043219588
  		"""
		# Conversion du Binaire603 en entier
		numberD = monBinD.toNumber()
		numberC = 0
		
		# Tant qu'il reste des bits à coder
		while numberD > 0:
			# On calcule le bloc à coder
			bloc = numberD % (1 << self.m_block_size)
			if verbose: print(f"bloc = {bloc} (en binaire : {Binaire603.fromNumber(bloc)})")

			# On décale number pour les prochains blocs
			numberD >>= (self.n - 1)**2
   
			# On code le bloc et on l'ajoute à numberC
			blocC = self.blocCode(bloc)
			numberC <<= (self.n)**2
			numberC += blocC
			if verbose: print(f"blocC = {blocC} (en binaire : {Binaire603.fromNumber(blocC)})")

		# On renvoie le résultat
		return Binaire603.fromNumber(numberC)

	def binDecode(self, monBinC:Binaire603) -> Binaire603:
		""" Renvoie le Binaire603 décodé à partir de monBinC
		>>> c = CodeurParite(8)
		>>> print(c.binDecode(c.binCode(Binaire603("Hey !"))).toString())
		Hey !
  		"""
		# Conversion du Binaire603 en entier
		numberC = monBinC.toNumber()
		numberD = 0

		# Tant qu'il reste des bits à décoder
		blocMod = (1 << (self.n)**2)
		while numberC > 0:
			# On calcule le bloc à décoder
			blocC = numberC % blocMod
   
			# On décale number pour les prochains blocs
			numberC >>= (self.n)**2
   
			# On décode le bloc et on l'ajoute à numberD
			bloc = self.blocDecode(blocC)
			numberD <<= (self.n - 1)**2
			numberD += bloc
		
		# On renvoie le résultat
		return Binaire603.fromNumber(numberD)
		



if __name__ == "__main__":
	import doctest
	doctest.testmod()

