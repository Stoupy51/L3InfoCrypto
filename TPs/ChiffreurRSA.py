
from math import log
from random import random,randint
from arithmetiqueDansZ import *
from Binaire603 import Binaire603
import tp_primes

from CodeurCA import CodeurCA

class ChiffreurRSA(CodeurCA):
    """"""
    def __init__(self, e = 73389317, d = 425656523868269, n = 2037223924932349):
        if isinstance(e, ChiffreurRSA):
            self.e = e.e
            self.d = e.d
            self.n = e.n
        else:
            if (e * d) % n != 1:
                raise ValueError("e et d ne sont pas inversibles modulo n")
            self.e = e
            self.d = d
            self.n = n
    
    def generateKeys():
        p = tp_primes.p[randint(0, tp_primes.pLen-1)]
        q = p
        while (p == q):
            q = tp_primes.p[randint(0, tp_primes.pLen-1)]
        n = p * q
        phi = (p - 1) * (q - 1)
        e = p
        while (e == p or e == q or PGCD(e, phi) != 1):
            e = tp_primes.p[randint(0, tp_primes.pLen-1)]
        d = ElementDeZnZ(e, phi).inverse()
        return (e, d, n)


    def __str__(self):
        return f"ChiffreurRSA avec clé '{self.privateKey} et {self.publicKey}'"
    def __repr__(self):
        return f"ChiffreurRSA({self.privateKey}, {self.publicKey})"


    def binCode(self, monBinD:Binaire603) -> Binaire603:
        """ Chiffre un message binaire en utilisant la clé publique
        >>> c = ChiffreurRSA()
        >>> c.binCode(Binaire603("Bonjour"))
        Binaire603([ 0x0a, 0x0a, 0x0a, 0x0a, 0x0a])
        """
        return Binaire603([ (b ** self.e) % self.n for b in monBinD ])

    def binDecode(self, monBinC:Binaire603) -> Binaire603:
        """
        """
        raise NotImplementedError


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(ChiffreurRSA.generateKeys())
