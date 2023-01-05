
from math import log
from random import random,randint
from arithmetiqueDansZ import *
from Binaire603 import Binaire603
from ChiffreurAffine import ChiffreurAffine

def crackAffine(Binaire603 : lb):
	"""
	>>> crack(Binaire603([ 0x03, 0x04, 0x05, 0x06, 0x01]))

	"""
	lf = lb.lFrequences().sort()

	### Tester tous les combinaisons de a et b
	#for a in range(1, 256, 3):
	#	for b in range(256):
	#		chiffreur = ChiffreurAffine(a,b)
	#		ldf = chiffreur.binDecode(lb).lFrequences()
	#		distance = 0
	
	# Méthode pour comparer les fréquences du français
	# avec le texte codé
	Ysp = lf.index(max(lf))
	Ye = lf.index(max(lf.pop(Ysp)))
	fr = bin603DepuisFichier("Les Miserables.txt").lFrequences()
	Xsp = lf.index(max(lf))
	Xe = lf.index(max(lf.pop(Xsp)))
	a, b = resolve(f"{Ysp} = a * {Ye} + b", f"{Ye} = a * {Xe} + b")
	return ChiffreurAffine(a,b)


def IndexOfMax(l):
	"""
	>>> IndexOfMax([1,2,3,4,5])
	4
	"""
	return 


