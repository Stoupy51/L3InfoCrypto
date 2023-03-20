
import numpy as np
from sympy import *
from arithmetiqueDansZ import *
from Binaire603 import Binaire603
from ChiffreurAffine import ChiffreurAffine

def crackAffine(lb: Binaire603, fFile: str = "Les Miserables.txt"):
	"""
	Méthode pour comparer les fréquences du français avec le texte codé
	formule :
	Ysp = (a * Xsp + b) % 256
	Ye = (a * Xe + b) % 256
	"""
	# Création de la liste des fréquences
	lf = lb.lFrequences()
	
	# Trouver les deux plus grandes fréquences (Space et E) pour le texte codé
	Ysp = lf.index(max(lf))
	lf.pop(Ysp)
	Ye = lf.index(max(lf))
	
	# Trouver les deux plus grandes fréquences (Space et E) pour le texte français
	fr = Binaire603.bin603DepuisFichier(fFile).lFrequences()
	Xsp = fr.index(max(fr))
	fr.pop(Xsp)
	Xe = fr.index(max(fr))

	# Résolution du système d'équations
	a, b = solve_system(Xsp, Ysp, Xe, Ye)
	return ChiffreurAffine(round(a), round(b))

def solve_system(Xsp, Ysp, Xe, Ye):
	"""Résout le système d'équations de fonction affine"""
	A = np.array([[Xsp, 1], [Xe, 1]])
	B = np.array([Ysp, Ye])
	return np.linalg.solve(A, B)



if __name__ == "__main__":

	# Crack Affine pour décoder Chiffre1.TXT
	f1 = Binaire603.bin603DepuisFichier("Chiffre1.TXT")
	c1 = crackAffine(f1)
	print(c1)
	print(c1.binDecode(f1).toString())
	

