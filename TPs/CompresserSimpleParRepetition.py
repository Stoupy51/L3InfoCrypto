
from Binaire603 import Binaire603
from CodeurCA import CodeurCA

class CompresserSimpleParRepetition(CodeurCA):
    """"""
    def __init__(self):
        pass

    def __str__(self):
        return f"CompresserSimpleParRepetition()"
    def __repr__(self):
        return f"CompresserSimpleParRepetition()"


    def binCode(self, monBinD:Binaire603) -> Binaire603:
        """
        Fonction qui compresse un binaire en utilisant la méthode de la répétition
        """
        monBinC = []
        previous = monBinD[0]
        count = 0
        for c in monBinD:
            if (c == previous and count < 255):
                count += 1
            else:
                monBinC += [count, previous]
                count = 0
                previous = c
        return Binaire603(monBinC)


    def binDecode(self, monBinC:Binaire603) -> Binaire603:
        """
        Fonction qui décompresse un binaire en utilisant la méthode de la répétition
        """
        assert len(monBinC) % 2 == 0, "Le binaire à décompresser doit être de longueur paire"
        monBin = []
        for pos in range(0, len(monBinC), 2):
            monBin += [monBinC[pos+1]] * monBinC[pos]
        return Binaire603(monBin)


    def demo():
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    CompresserSimpleParRepetition.demo()

