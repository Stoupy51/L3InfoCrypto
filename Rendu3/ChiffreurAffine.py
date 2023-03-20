
from math import log
from random import random,randint
from arithmetiqueDansZ import *
from Binaire603 import Binaire603

from CodeurCA import CodeurCA

class ChiffreurAffine(CodeurCA):
    """"""
    def __init__(self, a = 5, b = 10):
        if isinstance(a, ChiffreurAffine):
            self.b = a.b
        else:
            self.a = ElmtZnZ(a, 256)
            self.b = ElmtZnZ(b, 256)
            self.a_inv = self.a.inverse()

    def __str__(self):
        return f"Chiffreur Affine avec a = {self.a} et b = {self.b}"
    def __repr__(self):
        return f"ChiffreurAffine({self.a}, {self.b})"


    def binCode(self, monBinD:Binaire603) -> Binaire603:
        """
        >>> ChiffreurAffine(5, 7).binCode(Binaire603([ 0x01, 0x02, 0x03, 0x04, 0xFF]))
        Binaire603([ 0x0c, 0x11, 0x16, 0x1b, 0x02])
        >>> (ChiffreurAffine(7, 1564).binCode(Binaire603("Bonjour"))).toString()
        'ê%ĞĂ%O:'
        """
        return Binaire603([ (self.a * x + self.b) for x in monBinD ])


    def binDecode(self, monBinC:Binaire603) -> Binaire603:
        """
        >>> ChiffreurAffine(5, 7).binDecode(Binaire603([ 0x0c, 0x11, 0x16, 0x1b, 0x02]))
        Binaire603([ 0x01, 0x02, 0x03, 0x04, 0xff])
        """
        return Binaire603([ (y - self.b) * self.a_inv for y in monBinC ])


    def demo():
        monCodeur = ChiffreurAffine(5, 7)
        for k in range(3):
            monBin = Binaire603.exBin603(num = k, taille = 25)
            print("\nBin:", monBin)
            monBinCr = monCodeur.binCode(monBin)
            print("Bin Codée:", monBinCr)
            print("monBinCr décodé est égal à Monbin ?", monCodeur.binDecode(monBinCr) == monBin)

        montext = "Bonjour les amis !"
        lb = Binaire603(montext)
        chif = ChiffreurAffine(5, 7)
        lbc = chif.binCode(lb)
        lbd = chif.binDecode(lbc)
        print(f"\n{chif} a codé le texte '{montext}' en '{lbc.toString()}' et a décodé en '{lbd.toString()}' ")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    ChiffreurAffine.demo()

