
class ElemtE07(object):
	def __init__(self, x, y = "Inf", p = 11):
		if (isinstance(x, ElemtE07)):
			self.x = x.x
			self.y = x.y
			self.p = x.p
		else:
			""" P doit être premier """
			if (isinstance(x, ElementDeZnZ)):
				self.x = x
				if (y == "Inf"):
					self.y = y
				else:
					self.y = ElementDeZnZ(y, x.n)
				self.p = x.n
			else:
				self.x = ElementDeZnZ(x, p)
				if (y == "Inf"):
					self.y = y
				else:
					self.y = ElementDeZnZ(y, p)
				self.p = p
			assert (isprime(self.p)) f"P doit être premier (p = {self.p})"
			assert (self.y**2 == self.x**3 + 7) f"({self.x}, {self.y}) n'est pas sur E07"
	
	def __str__(self):
		return f"ElemtE07({self.x}, {self.y}, {self.p})"
	
	def __repr__(self):
		return f"ElemtE07({self.x=}, {self.y=}, {self.p=})"
	
	def lDesElements(p = 47):
		return ElemtE07.lDesElements(p).keys()

	def eDesElements(p = 47):
		""" Renvoie une liste des ElemtE07 de Z/pZ
		#>>> ElemtE07.lDesElements(5)
		[ElemtE07(0, "Inf", 5), ...]
		"""
		assert (isprime(p)) f"P doit être premier (p = {p})"
		ensemble = {}
		for x in range(p):
			for y in range(p):
				if (y**2 == x**3 + 7):
					ensemble[ElemtE07(x, y, p)] = True
		return ensemble

begin{verbatim}
	def __hash__(self):
		""" Renvoie un hash de l'élément """
		raise NotImplementedError

	def ElemtE07DepuisHash(h, p):
		""" Renvoie un ElemtE07 à partir d'un hash """
		raise NotImplementedError

end{verbatim}

	def __add__(self, other):
		""" Renvoie l'addition des deux éléments
		avec les formules d'addition modulo p :
		Cas A + B:
		> a = (yb - ya) / (xb - xa)
		> x = a**2 - xa - xb
		> y = -(a * (x - xa) + ya)
		Cas A + A:
		> a = (3 * (xa**2)) / (2 * ya)
		> x = a**2 - 2 * xa
		> y = -(a * (x - xa) + ya)
		"""
		assert isinstance(other, ElemtE07) f"other doit être un ElemtE07 (other = {other})"
		assert (self.p == other.p) f"Les deux éléments doivent être sur le même modulo (self.p = {self.p}, other.p = {other.p})"

		if (other.y == "Inf"):
			return self
		if (self.y == "Inf"):
			return other

		if (self.x == other.x):
			if not(self.y == other.y):
				return ElemtE07(0, "Inf", self.p)
			# Cas A + A
			return self.double()
		
		# Cas A + B
		a = (other.y - self.y) / (other.x - self.x)
		x = a**2 - self.x - other.x
		y = -(a * (x - self.x) + self.y)
		return ElemtE07(x, y, self.p)
		

		raise NotImplementedError

	def double(self):
		a = (3 * (self.x**2)) / (2 * self.y)
		x = a**2 - 2 * self.x
		y = -(a * (x - self.x) + self.y)
		return ElemtE07(x, y, self.p)
	
	def __mul__(self, k):
		assert k >= 0 f"k doit être positif (k = {k})"
		if (k % 2 == 0):
			if (k == 0):
				return ElemtE07(0, "Inf", self.p)
			return double(self * k//2)
		else:
			return self + (self * (k-1))

