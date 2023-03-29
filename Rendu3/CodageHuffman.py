
from Binaire603 import *
from CodeurCA import *
from Image603Etd import *
import Colors

class CodageHuffman(CodeurCA):
	""" Class CodageHuffman  """
	def __init__(self):
		pass

	def completeDico(self, arbre, prefix, dico):
		""" Remplis le dictionnaire récursivement en parcourant l'arbre
		Args:
			arbre (tuple): Arbre binaire sous forme de tuple
			prefix (_type_): Préfix du dictionnaire à ajouter
			dico (_type_): Dictionnaire à remplir
		Returns:
			dict: Dictionnaire rempli
		"""
		# Si l'arbre est un tuple
		if (isinstance(arbre, tuple)):

			# Si le premier élément du tuple est un tuple
			if isinstance(arbre[0], tuple):
				# On complète les deux branches de l'arbre
				dico = self.completeDico(arbre[0][0], prefix + "1", dico)
				dico = self.completeDico(arbre[0][1], prefix + "0", dico)
			
			# Sinon, c'est une feuille
			else:
				dico = self.completeDico(arbre[0], prefix, dico)
		
		# Sinon, c'est une feuille (un caractère)
		else:
			dico[chr(arbre)] = prefix
		
		# On retourne le dictionnaire
		return dico

	def listePonderee(self, liste):
		""" Transforme une liste de valeurs en une liste de couples (valeur, poids)
		Args:
			liste : liste de valeurs
		Returns:
			list : Liste de couples (valeur, poids)
		"""
		# On initialise la liste de couples
		l = []

		# Tant que la liste n'est pas vide
		while len(liste) > 0:

			# On récupère la première valeur de la liste
			i = liste[0]

			# Si la valeur n'est pas déjà dans la liste de couples
			if i not in l:

				# On ajoute le couple (valeur, poids) à la liste
				f = liste.count(i)
				l.append((i,f))

				# On supprime la valeur de la liste
				liste = [x for x in liste if x != i]
		return l

	def arbreDepuisListe(self, liste):
		""" Transforme une liste de valeurs en un arbre binaire
		Args:
			liste : liste de valeurs
		Returns:
			tuple : Arbre binaire sous forme de tuple
		
		>>> CodageHuffman().arbreDepuisListe([("A", 0.2), ("B", 0.3), ("C", 0.4)])
		((('C', 0.4), ((('A', 0.2), ('B', 0.3)), 0.5)), 0.9)
		>>> c = CodageHuffman()
		>>> c.printTuple(c.arbreDepuisListe([("A", 0.2), ("B", 0.3), ("C", 0.4)]), 0, False)
		(
		  (
		    (
		      'C'
		      '0.4'
		    ),
		    (
		      (
		        (
		          'A'
		          '0.2'
		        ),
		        (
		          'B'
		          '0.3'
		        ),
		      ),
		      '0.5'
		    ),
		  ),
		  '0.9'
		),
		"""
		# On récupère la liste pondérée (si ce n'est pas déjà le cas)
		if (isinstance(liste[0], tuple)):
			lP = liste
		else:
			lP = self.listePonderee(liste)
		
		# Tant que la liste de couples n'est pas sous la forme [(valeur, poids)] (arbre binaire)
		while len(lP) > 1:
			# On trie la liste de couples par poids
			lP.sort(key = lambda couple: couple[1])

			# On récupère les deux couples de poids les plus faibles
			l, r = lP.pop(0), lP.pop(0)

			# On crée un nouveau couple avec la somme des poids
			lP.append(((l, r), l[1] + r[1]))
		return lP[0]

	def printTuple(self, t, tab = 0, ch = True):
		""" Affiche un tuple de manière récursive pour faciliter la lecture de l'arbre """

		# Si le tuple est un tuple
		if isinstance(t, tuple):
			print("  " * tab + "(")
			self.printTuple(t[0], tab + 1)
			self.printTuple(t[1], tab + 1, False)
			print("  " * tab + "),")
		# Sinon, c'est une feuille
		else:
			# Si c'est un caractère
			if ch and isinstance(t, int):
				print("  " * tab + "'" + chr(t) + "'")
			else:
				print("  " * tab + "'" + str(t) + "'")


if __name__ == "__main__":
	import doctest
	doctest.testmod()

