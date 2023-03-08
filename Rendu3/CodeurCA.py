
from Binaire603 import *
class CodeurCA(object):
    """Un codeur doit surcharger les méthodes __init__ __repr__ __str__
    binCode, binDecode et codeurTest
    renvoyant et recevant un Binaire603
    C'est une forme de classe abstraites"""
    def __init__(self ):
        raise NotImplementedError # Ne pas toucher

    def __str__(self):
        raise NotImplementedError# Ne pas toucher
    def __repr__(self):
        raise NotImplementedError# Ne pas toucher

    def binCode(self,monBinD:Binaire603)->Binaire603:
        raise NotImplementedError# Ne pas toucher
    def binDecode(self,monBinC:Binaire603)->Binaire603:
        raise NotImplementedError# Ne pas toucher



if __name__ == "__main__":
    import doctest
    doctest.testmod()
##    monCodeur=CodeurCA() #A modifier si repris dans une classe en héritant
##    for k in range(5):
##        monBin=Binaire603.exBin603(num=k,taille=25)
##        print("Bin:",monBin)
##        monBinCr=monCodeur.binCode(monBin)
##        print("Bin Codée:",monBinCr)
##        print("monBinCr décodé est égal à Monbin ?",monCodeur.binDecode(monBinCr)==monBin)


