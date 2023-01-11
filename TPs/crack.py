
from math import log
from random import random,randint
import numpy as np
from sympy import *
from arithmetiqueDansZ import *
from Binaire603 import Binaire603
from ChiffreurAffine import ChiffreurAffine
from ChiffreurVigenere import ChiffreurVigenere
from ChiffreurParDecalage import ChiffreurParDecalage

def crackAffine(lb: Binaire603):
    lf = lb.lFrequences()

    ### Tester tous les combinaisons de a et b
    #for a in range(1, 256, 3):
    #    for b in range(256):
    #        chiffreur = ChiffreurAffine(a,b)
    #        ldf = chiffreur.binDecode(lb).lFrequences()
    #        distance = 0
    
    # Méthode pour comparer les fréquences du français
    # avec le texte codé
    # formule :
    # Ysp = (a * Xsp + b) % 256
    # Ye = (a * Xe + b) % 256
    Ysp = lf.index(max(lf))
    lf.pop(Ysp)
    Ye = lf.index(max(lf))
    fr = Binaire603.bin603DepuisFichier("../Les Miserables.txt").lFrequences()
    Xsp = fr.index(max(fr))
    fr.pop(Xsp)
    Xe = fr.index(max(fr))

    # Résolution du système d'équations
    a, b = solve_system(Xsp, Ysp, Xe, Ye)
    return ChiffreurAffine(round(a),round(b))

def solve_system(Xsp, Ysp, Xe, Ye):
    A = np.array([[Xsp, 1], [Xe, 1]])
    B = np.array([Ysp, Ye])
    return np.linalg.solve(A, B)

def crackVigenere(lb: Binaire603) : 
    return ChiffreurVigenere

if __name__ == "__main__":
    # Crack Affine
    f1 = Binaire603.bin603DepuisFichier("../Chiffre2.TXT")
    ca = crackAffine(f1)
    print(ca)   
    print(ca.binDecode(f1).toString())
