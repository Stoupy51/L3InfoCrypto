
import numpy as np
from sympy import *
from arithmetiqueDansZ import *
from Binaire603 import Binaire603

def crackInconnu(lb: Binaire603):
	""" Méthode de crack pour le chiffre inconnu """
	# Incomplète
	return None

if __name__ == "__main__":
    
    # Crack de Chiffre4.TXT
    f4 = Binaire603.bin603DepuisFichier("Chiffre4.TXT")
    c4 = crackInconnu(f4)
    print(c4)
    print(c4.binDecode(f4).toString())
    

