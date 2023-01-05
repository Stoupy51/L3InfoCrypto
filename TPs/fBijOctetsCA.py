


def fBijParDecalage(fBijObjectCA):
	"Une classe abstraite pour les bijections sur les octets"
	
	def __init__(self, decal):
		if (isinstance(decal, fBijObjectCA)):
			self.decal = decal.decal
		else:
			self.decal = ElementDeZnZ(decal, 256)

	def __repr__(self):
		return f"fBijParDecalage({self.decal})"
	
	def __call__(self, octet):
		return (octet + self.decal)
	
	def valInv(self, octet):
		"""Renvoie l'antécédent de octet"""
		return (octet - self.decal)

def fBijAffine(fBijObjectCA):
	"Une classe abstraite pour les bijections sur les octets"
	
	def __init__(self, a, b):
		if (isinstance(a, fBijObjectCA)):
			self.b = a.b
		else:
			self.a = ElementZnZ(a,255)
			self.b = ElementZnZ(b,255)
			self.a_inv = a.inverse()

	def __repr__(self):
		return f"fBijAffine({self.a}, {self.b})"
	
	def __call__(self, octet):
		return (self.a * octet + self.b)
	
	def valInv(self, octet):
		"""Renvoie l'antécédent de octet"""
		return (self.a_inv * (octet - self.b))
