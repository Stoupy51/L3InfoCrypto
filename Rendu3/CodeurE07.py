
from CodeurCA import *
from Binaire603 import *
from arithmetiqueDansZ import *
from ElemtE07Etd import *

class CodeurE0765537(CodeurCA):
	"""Codeur à partir de la courbe elliptique sur F65537"""
	def __init__(self, a = 17, B = ElemtE07(11,2,23), G = ElemtE07(19,9,23), p = 23):
		# Constructeur par copie
		if isinstance(a, CodeurE0765537):
			self.a = a.a
			self.A = a.A
			self.B = a.B
			self.G = a.G
			self.p = a.p
		# Constructeur par défaut
		else:
			self.a = a
			self.A = G * a
			self.B = B
			self.G = G
			self.p = p
			# Vérification de la validité des paramètres
			assert self.G.p == self.p, "Le point générateur n'est pas sur la courbe (p différent)"
			assert self.B.p == self.p, "Le point B n'est pas sur la courbe (p différent)"

	def __str__(self):
		return f"CodeurE0765537 avec la clé privé {self.a=} et sa clé publique {self.A=}, la clé publique d'un tier {self.B=}, avec comme point générateur {self.G=} sur F{self.p}"
	
	def __repr__(self):
		return f"CodeurE0765537({self.a}, {self.B}, {self.G}, {self.p})"
	
	def binCode(self, monBinD:Binaire603) -> list:
		""" Fonction qui chiffre un Binaire603 en utilisant la courbe elliptique sur F65537
		Args:
			monBinD : Binaire603 à chiffrer
		Returns:
			list : Liste d'élément chiffrés
		
		>>> CodeurE0765537(17).binCode(Binaire603("test"))
		[ElemtE07(19,14,23), ElemtE07(10,15,23), ElemtE07(19,14,23), ElemtE07(19,14,23)]
		"""
		# Initialisation de la liste qui contiendra le message chiffré
		monBinC = []
		aB = self.a * self.B

		# Pour chaque caractère du message
		for b in monBinD:
			# On convertit le caractère en un nombre
			m = ElemtE07.elemtE07APartirDeX(ElmtZnZ(b, self.p))
			# On chiffre le caractère
			c = m + aB
			# On ajoute l'élément chiffré à la liste
			monBinC.append(c)

		return monBinC
	
	def binDecode(self, monBinC:list)->Binaire603:
		""" Fonction qui déchiffre un Binaire603 en utilisant la courbe elliptique sur F65537
		Args:
			monBinC : Liste d'élément chiffrés
		Returns:
			Binaire603 : Binaire603 déchiffré
		
		>>> c = CodeurE0765537()
		>>> l = c.binCode(Binaire603("test"))
		>>> c.binDecode(l).toString()
		'test'
		"""
		# Initialisation de la liste qui contiendra le message déchiffré
		monBinD = []
		aB = self.a * self.B

		# Pour chaque élément de la liste
		for c in monBinC:
			# On déchiffre l'élément
			m = c - aB
			# On ajoute le caractère déchiffré à la liste
			monBinD.append(m.x.rep)

		# On retourne le message déchiffré
		return Binaire603(monBinD)

if __name__ == "__main__":
	import doctest
	doctest.testmod()

