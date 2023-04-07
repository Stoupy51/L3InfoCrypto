
from arithmetiqueDansZ import *

class PolF2(object):
	"Polynôme dans F2"

	def __init__(self, x, isMonome:bool = False):
		""" Défini par une liste d'ElmntZnZ ou un entier

		>>> print(PolF2([ElmtZnZ(1,2),0,1,0,1]))
		1 + x² + x⁴
		>>> print(PolF2(0b1000110010)) #Entier -> Polynome dans F2
		x + x⁴ + x⁵ + x⁹
		>>> PolF2(0)
		PolF2([ElmtZnZ(0,2)])
		"""
		# Constructeur par copie
		if isinstance(x, PolF2):
			self.data = x.data.copy()
			return
		
		# Cas d'un monôme créé par la méthode monome(i) (optimisation des calculs)
		if isMonome:
			self.data = [ElmtZnZ(1,2)] + [ElmtZnZ(0,2)]*x
			self.isMonome = True
			return

		# Si x est une liste
		if isinstance(x, list):

			# Création de la liste de données en mode inverse
			self.data = []
			for y in x:
				if (isinstance(y, int)):
					self.data.insert(0, ElmtZnZ(y, 2))
				elif (isinstance(y, ElmtZnZ)):
					self.data.insert(0, y)
				else:
					raise TypeError(f"Erreur : la liste passée en paramètre contient un élément qui n'est pas un entier ou un élément de ZnZ")
		
		# Si x est un entier
		elif isinstance(x, int):
			# Décomposition binaire de x (sans le 0b)
			binStr = bin(x)[2:]
			# Conversion en liste inversée
			self.data = [ElmtZnZ(int(y), 2) for y in binStr[::-1]]
		
		# Sinon, erreur
		else:
			raise TypeError(f"Erreur : le paramètre passé n'est pas une liste ou un entier")
		
		# Suppression des 0 en fin de liste dans tous les cas car on est gentil et on veut pas d'erreur
		while self.data[-1].rep == 0 and len(self.data) > 1:
			self.data.pop()
		
		# Indication si le polynôme est un monôme pour optimiser les calculs (un seul 1)
		compteur = self.data.count(ElmtZnZ(1, 2))
		self.isMonome = (compteur == 1)
		
		# Erreur si la liste est vide
		assert len(self.data) > 0, (f"Erreur : la liste passée en paramètre est vide")
	
	@staticmethod
	def monome(i):
		""" Création d'un monôme de degré i
		>>> print(PolF2.monome(2))
		x²
		"""
		return PolF2(i, isMonome = True)

	def degre(self):
		""" Retourne le degré du polynôme
		>>> PolF2(0b100011).degre()
		5
		"""
		return len(self.data) - 1

	def distanceHamming(self, other):
		""" Retourne la distance de Hamming entre deux polynômes : le nombre de coefficients différents
		>>> PolF2(0b100011).distanceHamming(PolF2(0b1100011))
		1
		>>> PolF2(0b100011).distanceHamming(PolF2(0b111))
		2
		"""
		assert isinstance(other, PolF2), f"Erreur : le paramètre passé n'est pas un polynôme dans F2"

		# Calcul de la différence de degré (0 si égaux, >0 si self plus grand, <0 si other plus grand)
		difference = self.degre() - other.degre()
		distance = 0

		# Si les deux polynômes ont le même degré, on compare terme à terme et on retourne la distance
		if difference == 0:
			for i in range(self.degre() + 1):
				if self.data[i] != other.data[i]:
					distance += 1
			return distance
		
		# Sinon, on ajoute des 0 en fin de liste à celui qui a le plus petit degré
		else:
			# Si self est plus grand, on ajoute des 0 en fin de liste à other
			if difference > 0:
				selfWithZeros = self.data
				otherWithZeros = other.data + [ElmtZnZ(0,2)] * difference
			# Sinon, on ajoute des 0 en fin de liste à self
			else:
				selfWithZeros = self.data + [ElmtZnZ(0,2)] * -difference
				otherWithZeros = other.data
			# On compare terme à terme et on retourne la distance
			for i in range(len(selfWithZeros)):
				if selfWithZeros[i] != otherWithZeros[i]:
					distance += 1
			return distance


	def __add__(self, other):
		""" Addition de deux polynômes dans F2 (@brief : c'est un XOR)

		>>> print(PolF2(0b100011) + PolF2(0b1100011))
		x⁶
		>>> print(PolF2(0b111100011)+ PolF2(0b100011))
		x⁶ + x⁷ + x⁸
		"""
		# Si le paramètre est un entier
		if isinstance(other, int):
			return PolF2(int(self) ^ other)
		# Si le paramètre est un polynôme
		elif isinstance(other, PolF2):
			return PolF2(int(self) ^ int(other))
		# Sinon, erreur
		else:
			raise TypeError(f"Erreur : le paramètre passé n'est pas un polynôme dans F2 ou un entier")

	def __radd__(self, other):
		return self + other
	def __sub__(self, other):
		return self + other
	def __rsub__(self, other):
		return self + other

	def __mul__(self, other):
		""" Multiplication de deux polynômes dans F2

		>>> print(PolF2.monome(2) * PolF2.monome(1))
		x³
		"""
		# Si le paramètre est un entier, on le convertit en polynôme
		if isinstance(other, int):
			other = PolF2(other)
		
		# Sinon, si le paramètre est un polynôme
		if isinstance(other, PolF2):
			# Si les deux polynômes sont des monômes, on crée un monôme de degré somme des degrés
			if self.isMonome and other.isMonome:
				return PolF2.monome(self.degre() + other.degre())


			# Si c'est un monôme, on décale juste les bits
			if other.isMonome:
				return PolF2(int(self) << other.degre())
			
			# Sinon, si self est un monôme, on décale juste les bits
			elif self.isMonome:
				return PolF2(int(other) << self.degre())
			
			# Sinon, on fait un produit de polynômes
			else:
				# Calcul du int du polynôme self en avance et initialisation du résultat
				selfInt = int(self)
				result = 0
				# Pour chaque bit de other.data
				for i in range(other.degre() + 1):
					# Si le bit est à 1, on ajoute à result le décalage de selfInt
					if other.data[i] == 1:
						result ^= selfInt << i
				return PolF2(result)
		else:
			raise TypeError(f"Erreur : le paramètre passé n'est pas un polynôme dans F2 ou un entier")

	def __rmul__(self, other):
		return self * other


	def __mod__(self, other):
		""" Calcul du reste de la division euclidienne de self par other

		>>> print(PolF2(0b11000101) % PolF2(0b11000))
		1 + x²
		"""
		# Initialisation des variables
		data = PolF2(self)
		otherDegre = other.degre()
		deg = data.degre()

		# Tant que le degré de data est supérieur ou égal au degré de other
		while deg >= otherDegre:
			# On calcule le monôme de degré (deg - otherDegre)
			monome = PolF2.monome(deg - otherDegre)

			# On soustrait à data le monôme * other
			data += other * monome

			# On met à jour le degré de data
			deg = data.degre()

		# On retourne le résultat
		return data

	def __floordiv__(self, other):
		""" Calcul du quotient de la division euclidienne de self par other
		>>> print(PolF2(0b11000101) // PolF2(0b11000))
		x³
		"""
		# Initialisation des variables
		monomes = []
		data = PolF2(self)
		otherDegre = other.degre()
		deg = data.degre()
  
		# Tant que le degré de data est supérieur ou égal au degré de other
		while deg >= otherDegre:
			# On calcule le monôme de degré (deg - otherDegre)
			monome = PolF2.monome(deg - otherDegre)
   
			# On ajoute le monôme à la liste des monomes
			monomes.append(monome)

			# On soustrait à data le monôme * other
			data += other * monome

			# On met à jour le degré de data
			deg = data.degre()

		# On retourne le résultat
		r = PolF2(0)
		for i in monomes:
			r += i
		return r


	def __int__(self):
		""" Conversion en entier
		>>> int(PolF2([ElmtZnZ(1,2), ElmtZnZ(0,2), ElmtZnZ(1,2)]))
		5
		"""
		# Initialisation des variables
		decalage = 0
		retour = 0

		# Pour chaque élément de la liste
		for i in self.data:

			# On ajoute la valeur de l'élément décalée à la valeur de retour
			retour += (i.rep << decalage)

			# On incrémente le décalage
			decalage += 1
		
		# On retourne la valeur de retour
		return retour

	def __str__(self):
		""" Conversion en chaîne de caractères
		>>> str(PolF2([ElmtZnZ(1,2), ElmtZnZ(0,2), ElmtZnZ(1,2)]))
		'1 + x²'
		"""
		# Initialisation de la chaîne de caractères
		retour = ""

		# Pour chaque élément de la liste
		for i in range(self.degre() + 1):
			# Si l'élément est à 1, on l'ajoute à la chaîne de caractères avec le bon exposant
			if self.data[i].rep == 1:
				if i == 0:
					retour += "1 + "
				else:
					retour += "x" + strExp(i) + " + "
		if retour == "":
			return "0"
		else:
			# On retourne la chaîne de caractères sans le dernier " + "
			return retour[:-3]

	def __repr__(self):
		""" Représentation de l'objet """
		return f"PolF2({self.data})"


if __name__ == "__main__":
	import doctest
	doctest.testmod()

