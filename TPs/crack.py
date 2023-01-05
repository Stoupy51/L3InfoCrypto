
from math import log
from random import random,randint
from sympy import *
from arithmetiqueDansZ import *
from Binaire603 import Binaire603
from ChiffreurAffine import ChiffreurAffine

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
    # Ysp = (a * Ye + b) % 256
    # Xsp = (a * Xe + b) % 256
    Ysp = lf.index(max(lf))
    lf.pop(Ysp)
    Ye = lf.index(max(lf))
    fr = Binaire603.bin603DepuisFichier("../Les Miserables.txt").lFrequences()
    Xsp = fr.index(max(fr))
    fr.pop(Xsp)
    Xe = fr.index(max(fr))

    print(f"Ysp = {Ysp}, Ye = {Ye}, Xsp = {Xsp}, Xe = {Xe}")

    # Résolution du système d'équations
    a, b = symbols('a b')
    eq1 = Eq(Ysp, (a * Ye + b) % 256)
    eq2 = Eq(Xsp, (a * Xe + b) % 256)
    s = solve((eq1, eq2))

    return ChiffreurAffine(s["a"],s["b"])

if __name__ == "__main__":
    f1 = Binaire603.bin603DepuisFichier("../Chiffre1.TXT")
    ca = crackAffine(f1)
    print(ca)
    print(ca.binDecode(f1))

