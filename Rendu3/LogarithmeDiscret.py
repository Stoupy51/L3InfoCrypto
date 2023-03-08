
import timeit
import Colors
from math import *
from arithmetiqueDansZ import *


def logarithmeDebile(a, b, p):
    """ TODO à fixer """
    previous = 1
    for i in range(p):
        previous = (previous * a) % p
        if previous == b:
            return i, None
        
    raise ArithmeticError("Pas de solution")


def LogarithmeDiscret(a, b, p):
    """
    Formules utilisées :
        x = i * m + j
        a^j = b * a^(-m)^i % p
    """

    # Si a n'est pas inversible, cette fonction ne fonctionne pas
    # On lance la version naïve
    a_inv = ElmtZnZ(a, p)
    if not a_inv.estInversible():
        return logarithmeDebile(a, b, p)
    
    # Initialisations
    liste = []
    m = int(sqrt(p)) + 1
    
    # Calcul de la liste des a ^ (-m) ^ i
    for i in range(m):
        ami = (a_inv ** (-m)) ** i
        liste.append((b * ami).rep)
    
    # Calcul de x en utilisant la liste
    for j in range(m):
        # Calcul de a^j
        aj = a ** j
        # Si a^j est dans la liste, on a trouvé mi + j
        # donc on peut calculer x et le retourner
        if aj in liste:
            i = liste.index(aj)
            return (m * i + j), liste
    
    raise ArithmeticError("Pas de solution")
    



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    # Exemple de calcul
    a, b, p = 2, 24, 97
    l, liste = LogarithmeDiscret(a, b, p)
    print(f"{Colors.green}x = {l} avec LogarithmeDiscret({a}, {b}, {p})")
    print(f"{Colors.green}Avec le dictionnaire : {Colors.orange}{liste}\n")
    
    # Comparaison des temps d'exécution
    a, b, p = 2, 24, 11777
    f = lambda: logarithmeDebile(a, b, p)
    print(f"{Colors.red}Temps d'exécution de 10 exécutions de logarithmeDebile :{Colors.orange}", round(timeit.timeit(f, number = 10), 3), "s")
    f = lambda: LogarithmeDiscret(a, b, p)
    print(f"{Colors.red}Temps d'exécution de 10 exécutions de LogarithmeDiscret :{Colors.orange}", round(timeit.timeit(f, number = 10), 3), "s")

