
from math import log
from random import random,randint
from arithmetiqueDansZ import *
from Binaire603 import Binaire603

from CodeurCA import CodeurCA

class ChiffreurAffine(CodeurCA):
    """"""
    def __init__(self, a = 1, b = 10):
        if isinstance(a, ChiffreurAffine):
            self.b = a.b
        else:
            self.a = ElementDeZnZ(a, 256)
            self.b = ElementDeZnZ(b, 256)
            self.a_inv = self.a.inverse()

    def __str__(self):
        return f"Chiffreur par décalage de {self.decal}"
    def __repr__(self):
        return f"ChiffreurAffine({self.decal})"


    def binCode(self, monBinD:Binaire603) -> Binaire603:
        """
        >>> ChiffreurAffine(2).binCode(Binaire603([ 0x01, 0x02, 0x03, 0x04, 0xFF]))
        Binaire603([ 0x03, 0x04, 0x05, 0x06, 0x01])
        >>> (ChiffreurAffine(1).binCode(Binaire603("Bonjour"))).toString()
        'Cpokpvs'
        """
        return Binaire603([ (self.a * x + self.b) % 256 for x in monBinD ])


    def binDecode(self, monBinC:Binaire603) -> Binaire603:
        """
        >>> ChiffreurAffine(2).binDecode(Binaire603([1,2,3,4,255]))
        Binaire603([ 0xff, 0x00, 0x01, 0x02, 0xfd])
        """
        return Binaire603([ (b - self.decal) % 256 for b in monBinC ])


    def demo():
        monCodeur=ChiffreurAffine(13)
        for k in range(3):
            monBin=Binaire603.exBin603(num=k,taille=25)
            print("Bin:",monBin)
            monBinCr=monCodeur.binCode(monBin)
            print("Bin Codée:",monBinCr)
            print("monBinCr décodé est égal à Monbin ?",monCodeur.binDecode(monBinCr)==monBin)

        montext='Bonjour les amis !'
        lb=Binaire603(montext)
        chif=ChiffreurAffine(1)
        lbc=chif.binCode(lb)
        lbd=chif.binDecode(lbc)
        print(f"{chif} a codé le texte '{montext}' en '{lbc.toString()}' et a décodé en '{lbd.toString()}' ")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    ChiffreurAffine.demo()

