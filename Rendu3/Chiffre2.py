
import numpy as np
from sympy import *
from arithmetiqueDansZ import *
from Binaire603 import Binaire603
from ChiffreurAffine import ChiffreurAffine

def crackAffineBruteForce(lb: Binaire603, fFile: str = "Les Miserables.txt", verbose: bool = False):
	"""
	Méthode brute pour comparer les fréquences du français avec le texte codé
	formule :
	Ysp = (a * Xsp + b) % 256
	Ye = (a * Xe + b) % 256
	"""
	# Création de la liste des fréquences et calculer Ysp (fréquence de 'Space') pour le texte codé
	lf = lb.lFrequences()
	Ysp = lf.index(max(lf))

	# Calculer Xsp et Xe (fréquence de 'Space' et 'E') pour le texte français
	fr = Binaire603.bin603DepuisFichier(fFile).lFrequences()
	Xsp = fr.index(max(fr))
	fr.pop(Xsp)
	Xe = fr.index(max(fr))

	# Verbose
	if (verbose):
		print(f"crackAffineBruteForce: Ysp = {Ysp}, Xsp = {Xsp}, Xe = {Xe}")
	
	### Tester tous les combinaisons de a et calculer b
	for a in range(1, 256, 2):
		# Calculer un possible b à partir de Ysp et Xsp
		b = (Ysp - a * Xsp) % 256

		# Créer un chiffreur affine avec a et b et vérifier si a est inversible
		chiffreur = ChiffreurAffine(a,b)
		if (chiffreur.a.estInversible()):

			# Calculer les fréquences pour le texte décodé
			ldf = chiffreur.binDecode(lb).lFrequences()
			
			# Calculer Dsp et De (fréquence de 'Space' et 'E') pour le texte décodé
			Dsp = ldf.index(max(ldf))
			ldf.pop(Dsp)
			De = ldf.index(max(ldf))
		
			# Vérifier si les fréquences sont les mêmes que celles du texte français
			if (Xsp == Dsp and Xe == De):
				return chiffreur
			elif verbose:
				print(f"crackAffineBruteForce: [Invalide] a = {a}, b = {b}, Dsp = {Dsp}, De = {De}")
	
	# Si aucune combinaison n'est trouvée, retourner un chiffreur négatif
	return ChiffreurAffine(-1,-1)


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

	# Crack Affine en Brute pour décoder Chiffre2.TXT car la méthode normale ne fonctionne pas
	f2 = Binaire603.bin603DepuisFichier("Chiffre2.TXT")
	c1 = crackAffineBruteForce(f2, verbose = True)
	print("\nChiffreur Affine trouvé :")
	print(c1)
	print(c1.binDecode(f2).toString())
	

