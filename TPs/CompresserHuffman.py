
from Binaire603 import *
from CodeurCA import *
from Image603Etd import *
import Colors

class CompresserHuffman(CodeurCA):
    """ Class CompresserHuffman  """
    def __init__(self):
        pass

    def __str__(self):
        return f"CompresserHuffman()"
    def __repr__(self):
        return f"CompresserHuffman()"
    

    def completeDico(self, arbre, prefix, dico):
        """Remplis le dictionnaire récursivement en parcourant l'arbre
        Args:
            arbre (tuple): Arbre binaire sous forme de tuple
            prefix (_type_): Préfix du dictionnaire à ajouter
            dico (_type_): Dictionnaire à remplir
        Returns:
            dict: Dictionnaire rempli
        """
        if (isinstance(arbre, tuple)):
            print("IF   arbre", arbre, "prefix", prefix)
            if isinstance(arbre[0], tuple):
                dico = self.completeDico(arbre[0][0], prefix + "1", dico)
                dico = self.completeDico(arbre[0][1], prefix + "0", dico)
            else:
                dico = self.completeDico(arbre[0], prefix, dico)
        else:
            print("ELSE arbre", chr(arbre), "prefix", prefix)
            dico[chr(arbre)] = prefix
        return dico

    def binCode(self, monBinD:Binaire603) -> Binaire603:
        """ Fonction qui compresse un Binaire603 en utilisant la méthode Huffman
        Args:
            monBinD : Binaire603 à compresser
        Returns:
            Binaire603 : Binaire603 compressé
        
        >>> CompresserHuffman().binCode(Binaire603("  d x x  x a  c b   b  a  "))
        None
        """
        a = arbreDepuisListe(monBinD)
        printTuple(a)
        dico = self.completeDico(a, "", {})
        print(dico)
        
        lbc = []
        for b in monBinD:
            lbc.append(dico[chr(b)])
        return Binaire603(lbc), dico


    def binDecode(self, monBinC:Binaire603) -> Binaire603:
        """
        """
        raise NotImplementedError


    def demo():
        pass

def listePonderee(liste):
    # c = len(liste)
    l = []
    while len(liste) > 0:
        i = liste[0]
        if i not in l:
            f = liste.count(i) # / c
            l.append((i,f))
            liste = [x for x in liste if x != i]
    return l

def arbreDepuisListe(liste):
    """ Transforme une liste de valeurs en un arbre binaire
    Args:
        liste : liste de valeurs
    Returns:
        tuple : Arbre binaire sous forme de tuple
    
    >>> arbreDepuisListe([("A", 0.2), ("B", 0.3), ("C", 0.4)])
    """
    if (isinstance(liste[0], tuple)):
        lP = liste
    else:
        lP = listePonderee(liste)

    ## TODO: Le nouveau doit être ajouté à la fin de la liste mais
    # quand même trié hein, genre un nouveau 2 dans [2, 2, 2] doit être le troisième
    while len(lP) > 1:
        lP.sort(key = lambda couple: couple[1])
        l, r = lP.pop(0), lP.pop(0)
        lP.append(((l,r), l[1] + r[1]))
    return lP[0]

def printTuple(t, tab = 0, ch = True):
    if isinstance(t, tuple):
        print("  " * tab + "(")
        printTuple(t[0], tab + 1)
        printTuple(t[1], tab + 1, False)
        print("  " * tab + "),")
    else:
        if ch:
            print("  " * tab + "'" + chr(t) + "'")
        else:
            print("  " * tab + "'" + str(t) + "'")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    CompresserHuffman.demo()

