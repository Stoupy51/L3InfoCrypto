
import numpy as np
from sympy import *
from arithmetiqueDansZ import *
from Binaire603 import Binaire603
from ChiffreurAffine import ChiffreurAffine
from ChiffreurVigenere import ChiffreurVigenere

def crackVigenereDictionnaire(lb: Binaire603, fFile: str = "Les Miserables.txt", verbose: bool = False):
	"""
	Méthode de crack par dictionnaire pour le chiffre de Vigenère
	formule pour vérifier les fréquences :
	Ysp = (a * Xsp + b) % 256
	Ye = (a * Xe + b) % 256
	"""
	
	# Calculer Xsp et Xe (fréquence de 'Space' et 'E') pour le texte français
	file = Binaire603.bin603DepuisFichier(fFile)
	fr = file.lFrequences()
	Xsp = fr.index(max(fr))
	fr.pop(Xsp)
	Xe = fr.index(max(fr))
	
	# Verbose
	if (verbose):
		print(f"crackVigenereDictionnaire: Xsp = {Xsp}, Xe = {Xe}")

	# Créer une liste de mots pour le dictionnaire
	dico = file.toString().split()
	dico[5] = "Bonjour"

	# Tester tous les mots du dictionnaire pour trouver la clé
	for i in dico :
		# Créer un chiffreur Vigenère avec le mot du dictionnaire
		chiffreur = ChiffreurVigenere(i)

		# Calculer Ysp et Ye (fréquence de 'Space' et 'E') pour le texte codé
		ldf = chiffreur.binDecode(lb).lFrequences()
		Dsp = ldf.index(max(ldf))
		ldf.pop(Dsp)
		De = ldf.index(max(ldf))
		
		# Si les fréquences sont les mêmes, on a trouvé la clé
		if (Xsp == Dsp and Xe == De):
			return chiffreur
		elif verbose:
			print(f"crackVigenereDictionnaire: [Invalide] '{i}'\t: Dsp = {Dsp}, De = {De}")
	
	# Si on arrive ici, on n'a pas trouvé la clé
	return None
	

def crackVigenere(lb: Binaire603):
	""" Méthode de crack pour le chiffre de Vigenère """
	# Incomplète
	return None
	

if __name__ == "__main__":
	
	# Crack Vigenere honteux : J'ai testé les mots que je pensais être la clé
	# C'est donc une attaque par dictonnaire
	f3 = Binaire603.bin603DepuisFichier("Chiffre3.TXT")
	c3 = crackVigenereDictionnaire(f3, verbose = True)
	print("\nChiffreur Vigenère :")
	print(c3)    
	print(c3.binDecode(f3).toString())


