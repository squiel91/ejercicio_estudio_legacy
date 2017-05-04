import re
import os
import csv
import shutil

from .instancia_prueba import InstanciaPrueba

# una prueba es un encabezado y una coleccion de ejercicios

class Prueba:
	def __init__(self, titulo, numero_instancias, encabezado=None):
		self.nombre = re.sub('[\W]', '', titulo.lower().replace(' ', '_'))
		self.titulo = titulo
		self.encabezado = encabezado
		self.numero_instancias = numero_instancias
		self.ejercicios = []

		self.instancias = []

	def agregar_ejercicio(self, ejercicio):
		self.ejercicios.append(ejercicio)

	def generar(self, tipo_exportacion):
		
		if tipo_exportacion == 'texto' or tipo_exportacion == 'latex':	
			directorio = self.nombre
			if os.path.exists(directorio):
				shutil.rmtree(directorio)
			os.mkdir(directorio)
			InstanciaPrueba.titulo = self.titulo

			for id in range(1, self.numero_instancias + 1):
				self.instancias.append(InstanciaPrueba(id, self.ejercicios))

			planilla_respuestas = [['id'] + [i + 1 for i in range(len(self.ejercicios))]]
			for prueba_individual in self.instancias:
				planilla_respuestas.append([prueba_individual.id] + prueba_individual.respuestas)
				if tipo_exportacion == 'texto':
					prueba_individual.exportar_texto(ruta=directorio)
				else:
					prueba_individual.exportar_latex(ruta=directorio)
			self.generar_csv_respuestas(planilla_respuestas, ruta=directorio)
		elif tipo_exportacion == 'eva':
			self.generar_eva_xml()
		else:
			raise Exception(tipo_exportacion + ' no se reconoce como un tipo de exportacion.')

	def generar_eva_xml(self):
		archivo_xml = open(self.nombre + '.xml', 'w')
		archivo_xml.write('''<?xml version="1.0" encoding="UTF-8"?>
			<quiz>
			<question type="category">
				<category>
					<text>$course$/{}</text>
				</category>
			</question>'''.format(self.titulo))
		for ejercicio in self.ejercicios:
			archivo_xml.write(ejercicio.eva_xml(self.numero_instancias))
		archivo_xml.write('</quiz>')
		archivo_xml.close()

	def generar_csv_respuestas(self, respuestas, ruta=''):
		csv_file = open(os.path.join(ruta, 'respuestas_correctas.csv'), 'w')
		csv_writer = csv.writer(csv_file, delimiter='\t')
		csv_writer.writerows(respuestas)
		csv_file.close()