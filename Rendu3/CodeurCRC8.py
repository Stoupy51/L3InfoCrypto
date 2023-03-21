
from PolF2 import *
from CodeurCA import *

class CodeurCRC8(CodeurCA):
	""" Classe définissant un codeur de CRC8 """
	def __init__(self, Pg = PolF2(0b110011011) ):
		""" Constructeur de la classe CodeurCRC8 """
		# Constructeur par copie
		if isinstance(Pg, CodeurCRC8):
			self.Pg = Pg.Pg
		elif isinstance(Pg, PolF2):
			self.Pg = Pg
		else:
			raise TypeError(f"Erreur : le paramètre passé n'est pas un polynôme dans F2")


	def blocCode(self, M, verbose: bool = False):
		""" Renvoie M codé en CRC avec un octet de plus
		>>> print(f"0x{CodeurCRC8().blocCode(0xab345678):x}")
		0xab34567821
  		"""
		# Création du polynôme à partir de M
		Ps = PolF2(M)

		# Calcul de Ps * X^r
		PsXr = Ps * PolF2.monome(self.Pg.degre())
  
		# Renvoie le nombre entier correspondant au polynôme PsXr + (PsXr % Pg)
		return int(PsXr + (PsXr % self.Pg))


	def estBlocValide(self, valc):
		""" Renvoie True si valc est un bloc valide, False sinon
		>>> CodeurCRC8().estBlocValide(0xab34567821)
		True
		>>> CodeurCRC8().estBlocValide(0xab34567820)
		False
		"""
		# On calcul le polynôme correspondant à valc
		poly = PolF2(valc)
  
		# True si le reste de la division euclidienne du polynome par Pg est nulle
		return int(poly % self.Pg) == 0


	def blocValideLePlusProche(self, valc):
		""" Renvoie le bloc valide le plus proche de valc
		>>> print(f"0x{CodeurCRC8().blocValideLePlusProche(0xab34567821):x}")
		0xab34567821
		>>> print(f"0x{CodeurCRC8().blocValideLePlusProche(0xab35567821):x}")
		0xab34567821
		"""
		# Méthode bourrine 1 : on inverse chaque bit et on teste si le bloc est valide
		# Problème : ça ne corrige qu'une seule erreur par bloc
		poly = PolF2(valc)
		for i in range(poly.degre()):
			# On inverse le bit i (en retenant l'ancienne valeur pour le remettre après)
			oldBit = poly[i].rep
			poly[i].rep = 1 - oldBit
   
			# Si le bloc est valide, on le renvoie
			if self.estBlocValide(int(poly)):
				return int(poly)

			# Sinon, on remet l'ancienne valeur
			else:
				poly[i].rep = oldBit

		# Erreur si aucun bloc valide n'a été trouvé
		raise ValueError("Erreur : aucune correction possible")


	def blocDecode(self, valc):
		"""
		>>> print(f"0x{CodeurCRC8().blocDecode(0xab34567821):x}")
		0xab345678
		>>> print(f"0x{CodeurCRC8().blocDecode(0xbb34567821):x}")
		0xab345678
		"""
		if self.estBlocValide(valc):
			return valc // self.Pg.degre()
		else:
			return self.blocValideLePlusProche(valc) // self.Pg.degre()


	def blocAvecErreur(val, nbBits = 32, nbErreurs = 1):
		""" Renvoie le bloc val avec nbErreurs bits changés
		"""
		# Création du polynôme à partir de val
		poly = PolF2(val)

		# On inverse les nbErreurs premiers bits
		for i in range(nbErreurs):
			poly[i].rep = 1 - poly[i].rep

		# Renvoie le nombre entier correspondant au polynôme
		return int(poly)


	def binCode(self, monBinD, verbose=True, nbErreurs=0):
		"""
		"""
		raise NotImplementedError


	def binDecode(self, monBinC):
		"""
		"""
		raise NotImplementedError


	def testDistance(self, nmax=0x101):
		"""Affiche la distance minimales entre les codage des blocs 0 ) nmax """
		raise NotImplementedError



if __name__ == "__main__":
	import doctest
	doctest.testmod()


