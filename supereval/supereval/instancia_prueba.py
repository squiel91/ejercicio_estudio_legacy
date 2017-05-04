import random
import os
import pdb
from pylatex import Document, NoEscape, Section

class InstanciaPrueba:
	def __init__(self, id, ejercicios): # aca le tengo que pasar el parametro encabezado
		self.id = id
		self.ejercicios_instanciados = [ejercicio.instanciar() for ejercicio in ejercicios]
		random.shuffle(self.ejercicios_instanciados)
		self.respuestas = []
		for ejercicio in self.ejercicios_instanciados:
			self.respuestas.append(ejercicio.respuesta_correcta)

	def exportar_texto(self, ruta=''): # deberia incluir el encabezado aca
		archivo_prueba = open(os.path.join(ruta, str(self.id) + '.txt'), 'w')
		archivo_prueba.write('{}\nIdentificador: {}\n\n'.format(InstanciaPrueba.titulo, self.id))
		for numero in range(0, len(self.ejercicios_instanciados)):
			archivo_prueba.write(self.ejercicios_instanciados[numero].text(numero + 1) + '\n')
		archivo_prueba.close()

	def exportar_latex(self, ruta=''):
		doc = Document()

		###### encabezado
		# import pdb
		
		# archi = open('caratula.tex', 'r')
		# archivo = [x for x in archi]
		# pdb.set_trace()
		# doc.append(NoEscape('Aca va a ir el encavesado'))

		###### encabezado
		
		with doc.create(Section('{} #{}'.format(InstanciaPrueba.titulo ,self.id))):
			for numero in range(0, len(self.ejercicios_instanciados)):
				doc.append(self.ejercicios_instanciados[numero].latex(numero + 1))

		doc.generate_pdf(os.path.join(ruta, str(self.id)), clean_tex=True)
