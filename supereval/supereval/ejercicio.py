import re
from .instancia_ejercicio import InstanciaEjercicio
from .formula import Formula
from .parametro import Parametro

simbolo_variable = '&'

class Ejercicio:

	def __init__(self):
		self.nombre = None
		self.titulo = None
		self.problema = None
		self.respuesta = None
		self.distractores = []

		self.parametros = {}
		self.formulas = {}
		self.formulas_ordenadas = []

	def set_titulo(self, titulo):
		self.titulo = titulo

	def set_problema(self, problema):
		self.problema = problema

	def set_solucion(self, respuesta):
		self.respuesta = respuesta

	def agregar_distractor(self, distractor):
		self.distractores.append(distractor)

	def agregar_parametro(self, nombre, minimo=0, maximo=100, decimales=2, conjunto=None):
		self.parametros[nombre] = Parametro(nombre, minimo, maximo, decimales, conjunto)

	def agregar_formula(self, nombre, computo, decimales=2): 
		nueva_formula = Formula(nombre, computo, decimales)
		self.formulas[nombre] = nueva_formula
		self.formulas_ordenadas.append(nueva_formula)

	def get_titulo(self):
		return self.titulo if self.titulo else 'Sin título'

	def numero_distractores(self):
		return len(self.distractores)

	def numero_parametros(self):
		return len(self.parametros)

	def numero_computos(self):
		return len(self.formulas)

	def instanciar(self):
		return InstanciaEjercicio(
				self.titulo, 
				self.problema, 
				self.respuesta, 
				self.distractores, 
				self.parametros, 
				self.formulas,
				self.formulas_ordenadas
			)

	def eva_xml(self, cantidad):
		ejercicio = '<question type="calculatedmulti">' # podria ser solo multi si no tiene parametros
		ejercicio += '<name><text>{}</text></name>'.format(self.titulo if self.titulo else 'Ejercicio')
		
		# parametros
		problema_eva = self.problema
		respuesta_eva = self.respuesta
		distractores_eva = self.distractores
		for parametro in self.parametros:
			problema_eva = re.sub(simbolo_variable + parametro + '(?=[\W]|$)', '{' + parametro + '}', problema_eva)
			respuesta_eva = re.sub(simbolo_variable + parametro + '(?=[\W]|$)', '{' + parametro + '}', respuesta_eva)
			for i in range(len(distractores_eva)):
				distractores_eva[i] = re.sub(simbolo_variable + parametro + '(?=[\W]|$)', '{' + parametro + '}', distractores_eva[i])
		
		# formulas
		formulas_procesadas = {}
		for formula in self.formulas_ordenadas:
			formula_parcial = formula.computo
			for parametro in self.parametros:
				formula_parcial = re.sub('(?:(?<=[\W])|(?<=^))' + parametro + '(?=[\W]|$)', '{' + parametro + '}', formula_parcial)
			for nombre_computo_parcial, computo in formulas_procesadas.items():
				formula_parcial = re.sub('(?:(?<=[\W])|(?<=^))' + nombre_computo_parcial + '(?=[\W]|$)', computo, formula_parcial)
			formula_eva = '{=' + convert_eva_operators(formula_parcial) + '}'
			formulas_procesadas[formula.nombre] = '(' + convert_eva_operators(formula_parcial) + ')'
			
			problema_eva = re.sub(simbolo_variable + formula.nombre + '(?=[\W]|$)', formula_eva, problema_eva)
			respuesta_eva = re.sub(simbolo_variable + formula.nombre + '(?=[\W]|$)', formula_eva, respuesta_eva)
			for i in range(len(distractores_eva)):
				distractores_eva[i] = re.sub(simbolo_variable + formula.nombre + '(?=[\W]|$)', formula_eva, distractores_eva[i])
		
		problema_eva = latex_to_eva_syntaxis(problema_eva)
		respuesta_eva = latex_to_eva_syntaxis(respuesta_eva)
		distractores_eva = [latex_to_eva_syntaxis(distractor_eva) for distractor_eva in distractores_eva]
		ejercicio += '<questiontext format="moodle_auto_format"><text><![CDATA[{}]]></text></questiontext>'.format(problema_eva)
		ejercicio += '''
			<generalfeedback format="moodle_auto_format"><text/></generalfeedback>
			<defaultgrade>1.0000000</defaultgrade>
			<penalty>0.3333333</penalty>
			<hidden>0</hidden>
			<synchronize>0</synchronize>
			<single>1</single>
			<answernumbering>abc</answernumbering>
			<shuffleanswers>1</shuffleanswers>
			<correctfeedback><text>Correcta.</text></correctfeedback>
			<partiallycorrectfeedback><text>Parcialmente correcto.</text></partiallycorrectfeedback>
			<incorrectfeedback><text>Incorrecto.</text></incorrectfeedback>'''
		ejercicio += '''
			<answer fraction="100">
				<text>{}</text>
				<tolerance>0.01</tolerance>
				<tolerancetype>1</tolerancetype>
				<correctanswerformat>1</correctanswerformat>
				<correctanswerlength>2</correctanswerlength>
				<feedback format="moodle_auto_format"><text/></feedback>
			</answer>'''.format(respuesta_eva)
		for distractor_eva in distractores_eva:
			ejercicio += '''
				<answer fraction="0">
					<text>{}</text>
					<tolerance>0.01</tolerance>
					<tolerancetype>1</tolerancetype>
					<correctanswerformat>1</correctanswerformat>
					<correctanswerlength>2</correctanswerlength>
					<feedback format="moodle_auto_format"><text/></feedback>
				</answer>'''.format(distractor_eva)
		ejercicio += '<dataset_definitions>'
		for parametro in self.parametros.values():
			ejercicio += parametro.eva_xml(cantidad)
		ejercicio += '</dataset_definitions>'
		ejercicio += '</question>'
		return ejercicio

def latex_to_eva_syntaxis(text):
	limites_latex_eva = re.sub(r'(?<!\\)\$\$([^$]*[^\\])\$\$', r'\n\n<p style="text-align: center;">\(\1\)</p>\n\n', text)
	limites_latex_eva = re.sub(r'(?<!\\)\$([^$]*[^\\])\$', r'\(\1\)', limites_latex_eva)
	sin_caracteres_escape = limites_latex_eva.replace('\\&', '&').replace('\\$', '$')
	return sin_caracteres_escape

def convert_eva_operators(formula):
	# ceil
	# floor
	# fmod
	# trunc
	# exp
	# log
	# pow
	# sqrt
	# acos
	# asin
	# atan
	# atan2
	# cos
	# hypot
	# sin
	# tan
	# acosh
	# asinh
	# atanh
	# cosh
	# sinh
	# tanh
	# fabs -> abs
	# degrees -> rad2deg
	# radians -> deg2rad
	# pi -> pi()
	# e -> exp(1)

	for python, php_equiv in {'pi': 'pi()', 'e': 'exp(1)', 'fabs': 'abs', 'degrees': 'rad2deg', 'radians': 'deg2rad'}.items():
		formula = re.sub('(?:(?<=[\W])|(?<=^))' + python + '(?=[\W]|$)', php_equiv, formula)
	return formula