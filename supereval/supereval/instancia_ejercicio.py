import random
import re

from pylatex import NoEscape, Subsection, Enumerate
import copy


simbolo_variable = '&'

def unpack_dict(a, b):
	new = copy.deepcopy(a)
	for c, v in b.items():
		new[c] = v
	return new

class InstanciaEjercicio:

	titulo = None

	def __init__(self, titulo, problema, respuesta, distractores, parametros, formulas, formulas_ordenadas):
		vars_instanciadas = {}
		for nombre, parametro in parametros.items():
			vars_instanciadas[nombre] = parametro.instanciar()

		vars_instanciadas_backup = vars_instanciadas.copy()

		form_instanciadas = {}
		for form in formulas_ordenadas:
			nombre = form.nombre 
			form_instanciadas[nombre] = form.instanciar(unpack_dict(vars_instanciadas, form_instanciadas))

		vars_instanciadas = vars_instanciadas_backup

		variables = unpack_dict(vars_instanciadas, form_instanciadas)

		self.problema = sustituir_variables(problema, variables)
		respuesta = sustituir_variables(respuesta, variables)
		distractores = [sustituir_variables(distractor, variables) for distractor in distractores]

		random.shuffle(distractores)

		self.posicion_respuesta = random.randint(0,len(distractores))

		self.respuesta_correcta = chr(self.posicion_respuesta + 97)

		self.opciones = distractores[:self.posicion_respuesta] + [respuesta] + distractores[self.posicion_respuesta:]

	def text(self, numero_ejercicio):
		latex_parcial = '{}.\n{}\n\n'.format(numero_ejercicio, self.problema)
		for i in range(len(self.opciones)):
			latex_parcial += '{}) {}\n'.format(chr(i + 97), self.opciones[i])
		return latex_parcial

	def latex(self, numero_ejercicio):
		ejercicio = Subsection('Ejercicio {}.'.format(numero_ejercicio))
		ejercicio.append(NoEscape('\\begin{flushleft}' + self.problema.replace('\n', '\linebreak \n') + '\end{flushleft}' ))
		with ejercicio.create(Enumerate(enumeration_symbol=r"\alph*)")) as enum:
			for opcion in self.opciones:
				enum.add_item(NoEscape(opcion.replace('\n', '\linebreak \n')))
		return ejercicio

def sustituir_variables(texto, variables):
	semi_sustituido = texto
	for nombre, valor in variables.items():
		semi_sustituido = re.sub(simbolo_variable + nombre + '(?=[\W]|$)', str(valor), semi_sustituido)
	return semi_sustituido
