
from Binaire603 import *
from CodeurCA import *
from Image603Etd import *
import Colors

class CompresserRLE(CodeurCA):
    """ Class CompresserRLE (RunLength Encoding) """
    def __init__(self, specialChar = 254):
        # If specialChar is a char, convert it to int
        if (isinstance(specialChar, str)):
            self.specialChar = ord(specialChar)
        else:
            self.specialChar = specialChar

    def __str__(self):
        return f"CompresserRLE()"
    def __repr__(self):
        return f"CompresserRLE()"


    def binCode(self, monBinD:Binaire603) -> Binaire603:
        """
        Fonction qui compresse un Binaire603 en utilisant la méthode RLE (RunLength Encoding)
        >>> CompresserRLE().binCode(Binaire603("Hey booooooomer"))
        Binaire603([ 0x48, 0x65, 0x79, 0x20, 0x62, 0xfe, 0x07, 0x6f, 0x6d, 0x65, 0x72])
        """
        # Initialisation des variables
        monBinC = []
        previous = monBinD[0]
        count = 0
        
		# Si le caractère spécial est le premier caractère, décaler le caractère
        if (previous == self.specialChar):
            previous += 1

		# Parcourir le binaire à compresser
        for i in range(len(monBinD)):
            c = monBinD[i]

            # Si le caractère spécial est rencontré, décaler le caractère
            if (c == self.specialChar):
                c += 1

            # Si le caractère est le même que le précédent
            # et que le compteur n'est pas à 255
            if (c == previous and count < 255):
                count += 1

            # Sinon, ajouter le compteur et le caractère précédent
            else:
                if (count < 3):
                    monBinC += [previous] * count
                else:
                    monBinC += [self.specialChar, count, previous]
                count = 1
                previous = c

        # Ajouter le dernier caractère
        if (count < 3):
            monBinC += [previous] * count
        else:
            monBinC += [self.specialChar, count, previous]

        return Binaire603(monBinC)


    def binDecode(self, monBinC:Binaire603) -> Binaire603:
        """
        Fonction qui décompresse un Binaire603 en utilisant la méthode RLE (RunLength Encoding)
        >>> CompresserRLE().binDecode(Binaire603([ 0x48, 0x65, 0x79, 0x20, 0x62, 0xfe, 0x17, 0x6f, 0x6d, 0x65, 0x72])).toString()
        'Hey booooooooooooooooooooooomer'
        """
        monBin = []

        i = 0
        # Parcourir le binaire à décompresser
        while (i < len(monBinC)):
            # Si le caractère spécial est rencontré, ajouter le caractère suivant le nombre de fois indiqué
            if (monBinC[i] == self.specialChar):
                monBin += [monBinC[i+2]] * monBinC[i+1]
                i += 3
            # Sinon, ajouter le caractère
            else:
                monBin += [monBinC[i]]
                i += 1
        # Retourner le binaire décompressé
        return Binaire603(monBin)


    def demo():
        files = ["../Coul10a.bmp", "../Coul10b.bmp"]
        compresseur = CompresserRLE()
        for file in files:
            
            print(Colors.orange + f"\nCompression de {file} :" + Colors.reset)
            img = Image603.imgDepuisBmp(file, verbose = False)
            imgBinaire = img.toBinaire603()
            c = compresseur.binCode(imgBinaire)
            d = compresseur.binDecode(c)
            
            percentage = len(c) / len(imgBinaire)
            print(f"Compression de {len(imgBinaire)} octets en {len(c)} octets soit {percentage:.3%} de la taille originale")
            
            if (imgBinaire == d):
                voulu = "Le fichier a perdu du poids"
                if percentage > 1:
                    voulu = Colors.blue + "Le fichier a augmenté de taille"
                # Print in green
                print(Colors.green + f"Compression réussie : {voulu}" + Colors.reset)
            else:
                # Print in red
                print(Colors.red + f"Compression échouée : \nLa longueur après compression et décompression est de {len(d)} au lieu de {len(imgBinaire)}" + Colors.reset)
                print(imgBinaire)
                print(d)
                #img.affiche()
                #img2 = Image603.fromBinaire603(d)
                #img2.affiche()
        
        files = ["../BelAmi.TXT", "../Bovary.TXT", "../Germinal.txt", "../Guerre et Paix.txt", "../Les Miserables.txt"]
        # files = []
        for file in files:
            
            print(Colors.orange + f"\nCompression de {file} :" + Colors.reset)
            texte = Binaire603.bin603DepuisFichier(file)
            c = compresseur.binCode(texte)
            d = compresseur.binDecode(c)
            
            percentage = len(c) / len(texte)
            print(f"Compression de {len(texte)} octets en {len(c)} octets soit {percentage:.3%} de la taille originale")
            
            if (texte == d):
                voulu = "Le fichier a perdu du poids"
                if percentage > 1:
                    voulu = Colors.blue + "Le fichier a augmenté de taille"
                # Print in green
                print(Colors.green + f"Compression réussie : {voulu}" + Colors.reset)
            else:
                # Print in red
                print(Colors.red + f"Compression échouée : \nLa longueur après compression et décompression est de {len(d)} au lieu de {len(texte)}" + Colors.reset)
                #print(texte.toString())
                #print(d.toString())
        


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    CompresserRLE.demo()

