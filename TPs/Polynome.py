from arithmetiqueDansZ import *

class Polynome(object):
    "Polynome"
    
    def __init__(self, coeff = ElementDeZnZ(1,2), expo = 1):
        """
        >>> Polynome(ElementDeZnZ(1,2),2)
        Polynome(ElementDeZnZ(1,2),2)
        >>> Polynome(Polynome(ElementDeZnZ(1,2),10))
        Polynome(ElementDeZnZ(1,2),10)
        """
        
        if (isinstance(coeff, Polynome)) :
            self.listPolynome = coeff.listPolynome
        else :
            # liste de tuples (coeff, expo) enregistrant les termes du polynome
            self.listPolynome = set()
            # ajout du premier terme
            self.listPolynome.add((coeff, expo))
        
    def __str__(self):
        """
        >>> print(ElementDeZnZ(1,2),2)
        x^2
        """
        
        polynomestr = ""
        
        # parcours de la liste des termes du polynome
        for i in range(len(self.listPolynome)):
            # recuperation du coefficient et de l'exposant
            coeff, expo = self.listPolynome[i]
            # ajout du terme au polynome sous forme de chaine de caracteres
            if coeff == 1:
                polynomestr += "x^" + str(expo)
            if coeff == 1 and expo == 1:
                polynomestr += "x"
            if coeff == 1 and expo == 0:
                polynomestr += "1"
            if expo == 1:
                polynomestr += int(coeff) + "x"
            if expo == 0:
                polynomestr += int(coeff)
            else : 
                polynomestr += int(coeff) + "x^" + str(expo)
            # ajout du signe si il y a un terme suivant
            if i < len(self.listPolynome) - 1:
                # verification si le terme suivant est positif
                if self.listPolynome[i+1][0] > 0:
                    polynomestr += " + "
                else :
                    polynomestr += " - "
    
    def __repr__(self):
        """
        >>> Polynome(ElementDeZnZ(1,2),2)
        Polynome({(ElementDeZnZ(1,2),2)})
        """
        return f"Polynome({self.listPolynome})"
    
    def __add__(self,other):
        """
        >>> Polynome(ElementDeZnZ(1,4),2) + Polynome(ElementDeZnZ(1,4),2)
        Polynome({(ElementDeZnZ(2,4),2)})
        >>> Polynome(ElementDeZnZ(1,2),2) + Polynome(ElementDeZnZ(1,4),3)
        Polynome({(ElementDeZnZ(1,2),2), (ElementDeZnZ(1,4),3)})
        """
        # copie du polynome courant
        polynome = Polynome(self.listPolynome)
        otherPol = Polynome(other)
        
        # On verifie que l'objet est bien un polynome
        if isinstance(otherPol, Polynome) :
            # On parcours les termes du polynome courant
            for i in range(len(polynome.listPolynome)):
                # On recupere le coefficient et l'exposant
                coeff, expo = polynome.listPolynome[i]
                # On parcours les termes du polynome a ajouter
                for j in range(len(otherPol.listPolynome)):
                    # On recupere le coefficient et l'exposant
                    coeff2, expo2 = otherPol.listPolynome[j]
                    # On verifie si les exposants sont egaux
                    if expo == expo2:
                        # On ajoute les coefficients
                        coeff += coeff2
                        # On supprime le terme du polynome a ajouter
                        otherPol.listPolynome.remove((coeff2, expo2))
                        # Si le coefficient est nul, on supprime le terme du polynome courant
                        if coeff == 0:
                            coeffPol, expoPol = polynome.listPolynome[j]
                            polynome.listPolynome.remove((coeff, expo))
                        else :
                            # On met a jour le terme du polynome courant
                            polynome.listPolynome[i] = (coeff, expo)
            # On ajoute les termes restants du polynome a ajouter
            for i in range(len(otherPol.listPolynome)):
                polynome.listPolynome.add(otherPol.listPolynome[i])
            return polynome
        else :
            raise TypeError("L'objet n'est pas un polynome")


    def __radd__(self,other):
        """
        >>> Polynome(ElementDeZnZ(1,4),2) + Polynome(ElementDeZnZ(1,4),2)
        Polynome({(ElementDeZnZ(2,4),2)})
        >>> Polynome(ElementDeZnZ(1,2),2) + Polynome(ElementDeZnZ(1,4),3)
        Polynome({(ElementDeZnZ(1,2),2), (ElementDeZnZ(1,4),3)})
        """
        return Polynome.__add__(self, other)
    
    def __neg__(self):
        """
        >>> -Polynome(ElementDeZnZ(1,4),2)
        Polynome({(ElementDeZnZ(3,4),2)})
        """
        # copie du polynome courant
        polynome = Polynome(self.listPolynome)
        
        # On parcours les termes du polynome courant
        for i in range(len(polynome.listPolynome)):
            # On recupere le coefficient et l'exposant
            coeff, expo = polynome.listPolynome[i]
            # On met a jour le terme du polynome courant
            polynome.listPolynome[i] = (-coeff, expo)
            
        return polynome
    
    def __sub__(self,other):
        """
        >>> Polynome(ElementDeZnZ(1,4),2) - Polynome(ElementDeZnZ(1,4),2)
        Polynome(set())
        """
        return Polynome.__add__(self, -other)

    def __rsub__(self,other):
        """
        >>> Polynome(ElementDeZnZ(1,4),2) - Polynome(ElementDeZnZ(1,4),2)
        Polynome(set())
        """
        return Polynome.__add__(-self, other)

    def __mul__(self,other):
        """
        
        """
        polynome = Polynome()
        
        # On verifie que l'objet est bien un polynome
        if isinstance(other, Polynome) :
            # TODO
            return polynome

    def __rmul__(self,other):
        """
        
        """
        return Polynome.__mul__(self, other)
    
    def __eq__(self, other):
        """
        >> Polynome(ElementDeZnZ(1,4),2) == Polynome(ElementDeZnZ(1,4),2)
        True
        """
        if isinstance(other, ElementDeZnZ):
            return self.listPolynome == other.listPolynome # TODO à revoir
        
        return False
    
    def __div__(self, other):
        return self.__floordiv__(other)

    def __floordiv__(self,other):
        """
        
        """
        polynome = Polynome()
        
        # On verifie que l'objet est bien un polynome
        if isinstance(other, Polynome) :
            # TODO
            return polynome
        
        raise TypeError("L'objet n'est pas un polynome")
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()