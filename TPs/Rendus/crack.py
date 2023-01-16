
from math import log
from random import random,randint
import numpy as np
from sympy import *
from arithmetiqueDansZ import *
from Binaire603 import Binaire603
from ChiffreurAffine import ChiffreurAffine
from ChiffreurVigenere import ChiffreurVigenere
from ChiffreurParDecalage import ChiffreurParDecalage

def crackAffine(lb: Binaire603, fFile: str = "Les Miserables.txt"):
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
    fr = Binaire603.bin603DepuisFichier(fFile).lFrequences()
    Xsp = fr.index(max(fr))
    fr.pop(Xsp)
    Xe = fr.index(max(fr))

    # Résolution du système d'équations
    a, b = solve_system(Xsp, Ysp, Xe, Ye)
    return ChiffreurAffine(round(a),round(b))

def solve_system(Xsp, Ysp, Xe, Ye):
    """Résout le système d'équations de fonction affine"""
    A = np.array([[Xsp, 1], [Xe, 1]])
    B = np.array([Ysp, Ye])
    return np.linalg.solve(A, B)

def crackVigenere(lb: Binaire603): 
    return ChiffreurVigenere

if __name__ == "__main__":
    # Crack Affine
    f1 = Binaire603.bin603DepuisFichier("Chiffre1.TXT")
    c1 = crackAffine(f1)
    print(c1)
    print(c1.binDecode(f1).toString())
    
    f2 = Binaire603.bin603DepuisFichier("Chiffre2.TXT")
    c2 = crackAffine(f2)
    print(c2)
    print(c2.binDecode(f2).toString())
    
    f3 = Binaire603.bin603DepuisFichier("Chiffre3.TXT")
    c3 = crackAffine(f3)
    print(c3)
    print(c3.binDecode(f3).toString())
    
    f4 = Binaire603.bin603DepuisFichier("Chiffre4.TXT")
    c4 = crackAffine(f4)
    print(c4)
    print(c4.binDecode(f4).toString())
    
    
    print("\n\n\nRappel des chiffreurs trouvés :")
    print("Chiffre1.TXT :", c1)
    print("Chiffre2.TXT :", c2)
    print("Chiffre3.TXT :", c3)
    print("Chiffre4.TXT :", c4)
    

