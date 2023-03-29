
from Binaire603 import *
from CodeurCA import *
from Image603Etd import *
from CodageHuffman import *
import Colors

class CompresserHuffman(CodeurCA):
	""" Class CompresserHuffman  """
	def __init__(self):
		self.c = CodageHuffman()

	def __str__(self):
		return f"CompresserHuffman()"
	def __repr__(self):
		return f"CompresserHuffman()"

	def binCode(self, monBinD:Binaire603) -> list:
		""" Fonction qui compresse un Binaire603 en utilisant la méthode Huffman
		Args:
			monBinD : Binaire603 à compresser
		Returns:
			list : Binaire603 compressé
		
		>>> CompresserHuffman().binCode(Binaire603("  d x x  x a  c b   b  a  "))
		(['0', '0', '1011', '0', '100', '0', '100', '0', '0', '100', '0', '111', '0', '0', '1010', '0', '110', '0', '0', '0', '110', '0', '0', '111', '0', '0'], {'a': '111', 'b': '110', 'd': '1011', 'c': '1010', 'x': '100', ' ': '0'})
		"""
		# On récupère un arbre binaire à partir du Binaire603
		a = self.c.arbreDepuisListe(monBinD)

		# On récupère un dictionnaire à partir de l'arbre binaire
		dico = self.c.completeDico(a, "", {})
		
		# On initialise la liste de caractères compressés
		lbc = []
		for b in monBinD:
			lbc.append(dico[chr(b)])

		# On renvoie le Binaire603 compressé et le dictionnaire
		return lbc, dico


	def binDecode(self, monBinC:list, dico) -> Binaire603:
		""" Fonction qui décompresse un Binaire603 en utilisant la méthode Huffman
		Args:
			monBinC : Binaire603 compressé (à décompresser)
		Returns:
			Binaire603 : Binaire603 décompressé
		
		>>> c = CompresserHuffman()
		>>> monBinD = Binaire603("  d x x  x a  c b   b  a  ")
		>>> monBinC, dico = c.binCode(monBinD)
		>>> print(f"'{c.binDecode(monBinC, dico).toString()}'")
		'  d x x  x a  c b   b  a  '
		"""
		# Initialisation du Binaire603 décompressé et inversement du dictionnaire (clé, valeur)
		bd = ""
		dicoInv = {v: k for k, v in dico.items()}

		# On parcourt le Binaire603 compressé
		for b in monBinC:
			# On ajoute le caractère décompressé au Binaire603
			char = dicoInv[b]
			bd += char
		
		# On renvoie le Binaire603 décompressé
		return Binaire603(bd)


	def demo():
		pass


if __name__ == "__main__":
	import doctest
	doctest.testmod()
	CompresserHuffman.demo()

