
from math import log
from random import random,randint
from arithmetiqueDansZ import *
from Binaire603 import Binaire603

from CodeurCA import CodeurCA

class ChiffreurVigenere(CodeurCA):
    """"""
    def __init__(self, key = "Bonjour les amis"):
        if isinstance(key, ChiffreurVigenere):
            self.key = key.key
            self.keySize = key.keySize
        else:
            self.key = key
            self.keySize = len(key)

    def __str__(self):
        return f"ChiffreurVigenere de avec clé '{self.key}'"
    def __repr__(self):
        return f"ChiffreurVigenere('{self.key}')"


    def binCode(self, monBinD:Binaire603) -> Binaire603:
        """
        >>> ChiffreurVigenere("bonjour").binCode(Binaire603([ 0x01, 0x02, 0x03, 0x04, 0xFF]))
        Binaire603([ 0x63, 0x71, 0x71, 0x6e, 0x6e])
        >>> (ChiffreurVigenere("bonjour").binCode(Binaire603("Bonjour"))).toString()
        '¤ÞÜÔÞêä'
        """
        r = []
        i = 0
        for b in monBinD:
            r.append((b + ord(self.key[i])) % 256)
            i = (i + 1) % self.keySize
        return Binaire603(r)


    def binDecode(self, monBinC:Binaire603) -> Binaire603:
        """
        >>> ChiffreurVigenere("bonjour").binDecode(Binaire603([1,2,3,4,255]))
        ???
        """
        r = []
        i = 0
        for b in monBinC:
            r.append((b - ord(self.key[i])) % 256)
            i = (i + 1) % self.keySize
        return Binaire603(r)


    def demo():
        """monCodeur=ChiffreurVigenere(13)
        for k in range(3):
            monBin=Binaire603.exBin603(num=k,taille=25)
            print("Bin:",monBin)
            monBinCr=monCodeur.binCode(monBin)
            print("Bin Codée:",monBinCr)
            print("monBinCr décodé est égal à Monbin ?",monCodeur.binDecode(monBinCr)==monBin)

        montext='Bonjour les amis !'
        lb=Binaire603(montext)
        chif=ChiffreurVigenere(1)
        lbc=chif.binCode(lb)
        lbd=chif.binDecode(lbc)
        print(f"{chif} a codé le texte '{montext}' en '{lbc.toString()}' et a décodé en '{lbd.toString()}' ")
        """
        return


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    ChiffreurVigenere.demo()

