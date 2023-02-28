
from Binaire603 import *
from arithmetiqueDansZ import *
from ElemtE07Etd import *

class CodeurE0765537(object):
	"""Codeur à partir de la courbe elliptique sur F65537"""
	def __init__(self, a, B = ElemtE07(47106,21934,65537), G = ElemtE07(47106,21934,65537), p = 65537):
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
	
	def binCode(self, monBinD:Binaire603)->Binaire603:
		""" Fonction qui chiffre un Binaire603 en utilisant la courbe elliptique sur F65537
		Args:
			monBinD : Binaire603 à chiffrer
		Returns:
			Binaire603 : Binaire603 chiffré
		
		>>> CodeurE0765537(47106).binCode(Binaire603("test")).toNumber()
		13036898041474994413324356361039415141793793
		"""
		# On convertit le message en binaire en un nombre
		m = monBinD.toNumber()
		# On chiffre le message
		c = self.B * m
		# On convertit le chiffre en binaire
		return Binaire603.fromNumber(c.__hash__())
	
	def binDecode(self, monBinC:Binaire603)->Binaire603:
		""" Fonction qui déchiffre un Binaire603 en utilisant la courbe elliptique sur F65537
		Args:
			monBinC : Binaire603 à déchiffrer
		Returns:
			Binaire603 : Binaire603 déchiffré
		
		>>> c = CodeurE0765537(47106)
		>>> n = c.binCode(Binaire603("test")).toNumber()
		>>> c.binDecode(Binaire603.fromNumber(n)).toString()
		'test'
		"""
		# On convertit le chiffre en binaire en un nombre
		c = ElemtE07.ElemtE07DepuisHash(monBinC.toNumber())
		# On déchiffre le chiffre 
		"""(bugué car multiplication de ElemtE07 par un autre ElemtE07)"""
		m = self.A * c
		# On convertit le message en binaire
		return Binaire603.fromNumber(m)

if __name__ == "__main__":
	import doctest
	doctest.testmod()

