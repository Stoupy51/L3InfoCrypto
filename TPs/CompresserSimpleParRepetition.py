
from Binaire603 import *
from CodeurCA import *
from Image603Etd import *

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
        >>> CompresserSimpleParRepetition().binCode(Binaire603("00011110000011111111"))
        Binaire603([ 0x03, 0x30, 0x04, 0x31, 0x05, 0x30, 0x08, 0x31])
        >>> CompresserSimpleParRepetition().binCode(Binaire603("00011110000011111111")).toString()
        'ă0Ą1ą0Ĉ1'
        """
        monBinC = []
        previous = monBinD[0]
        count = 0
        for c in monBinD:
            if (c == previous and count < 255):
                count += 1
            else:
                monBinC += [count, previous]
                count = 1
                previous = c
        monBinC += [count, previous]
        return Binaire603(monBinC)


    def binDecode(self, monBinC:Binaire603) -> Binaire603:
        """
        Fonction qui décompresse un binaire en utilisant la méthode de la répétition
        >>> CompresserSimpleParRepetition().binDecode(Binaire603("ă0Ą1ą0Ĉ1")).toString()
        '00011110000011111111'
        """
        assert len(monBinC) % 2 == 0, "Le binaire à décompresser doit être de longueur paire"
        monBin = []
        for pos in range(0, len(monBinC), 2):
            monBin += [monBinC[pos+1]] * monBinC[pos]
        return Binaire603(monBin)


    def demo():
        files = ["../Coul10a.bmp", "../Coul10b.bmp"]
        compresseur = CompresserSimpleParRepetition()
        for file in files:
            
            print(f"\nCompression de {file} :")
            img = Image603.imgDepuisBmp(file, verbose = False)
            imgBinaire = img.toBinaire603()
            c = compresseur.binCode(imgBinaire)
            d = compresseur.binDecode(c)
            
            percentage = len(c)/len(imgBinaire)
            print(f"Compression : {len(c)} bits")
            print(f"{len(c)} / {len(imgBinaire)} = {percentage:.3%}")
            
            if (imgBinaire == d):
                # Print in green
                print(f"\033[92mCompression réussie\033[0m")
            else:
                # Print in red
                print(f"\033[91mCompression échouée\033[0m")
        


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    CompresserSimpleParRepetition.demo()

