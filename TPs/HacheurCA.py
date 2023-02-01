
from Binaire603 import Binaire603

class HacheurCA(object):

    def __init__(self,nbBits=128):
         self.nbBits=nbBits
         self.valMod=2**nbBits
    def __str__(self):
        return f"Classe abstraite Hacheur CA sur {self.nbBits} bits" # A surcharger dans une classe fille
    def __repr__(self):
        return "HacheurCA({self.nbBits})"# A surcharger dans une classe fille

    def __call__(self,monBinC:Binaire603):
        """Renvoie la valeur du hash"""
        s=0
        for b in monBinC:
            s=s+b
        return s % self.valMod

if __name__ == "__main__":
    import doctest
    doctest.testmod()


