import math

class Formula:
	def __init__(self, nombre, computo, decimales):
		self.nombre = nombre
		self.computo = computo
		self.decimales = decimales or 2
		
	def instanciar(self, vars_instanciadas):
		{**math.__dict__, **{'e':1}}['e']
		self.evaluacion = round(eval(self.computo, {**math.__dict__, **vars_instanciadas}), self.decimales)
		return self.evaluacion

	def __str__(self):
		self.instanciar()
		return self.nombre + ':' + str(self.decimales) + ':' +str(self.evaluacion)