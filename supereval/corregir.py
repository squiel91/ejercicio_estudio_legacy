import csv
import argparse

def corregir(respuestas_correctas, respuestas_alumnos, planilla_correciones):
	
	if not planilla_correciones:
		planilla_correciones = 'planilla_correciones.csv'
	respuestas_alumnos = csv_a_array(respuestas_alumnos, 1)
	respuestas_correctas = csv_a_array(respuestas_correctas, 1)
	
	respuestas_correctas_dict = {}
	for respuesta_correcta in respuestas_correctas:
		respuestas_correctas_dict[respuesta_correcta[0]] = respuesta_correcta[1:]

	num_problemas = len(respuestas_correctas[1:])
	
	correcciones = [['id', 'alumno', 'nota'] + list(range(1, num_problemas))] # range?

	for respuestas_alumno in respuestas_alumnos:
		correccion_prueba = respuestas_alumno[:2] + ['NOTA']
		respuestas_correcta_prueba = respuestas_correctas_dict[respuestas_alumno[0]]
		nota = 0
		for i in range(num_problemas -1):
			if respuestas_correcta_prueba[i] == respuestas_alumno[i+2]:
				# respuesta correcta
				correccion_prueba.append('')
				nota += 1
			else:
				# respuesta incorrecta
				correccion_prueba.append('X')
		
		correccion_prueba[2] = nota
		correcciones.append(correccion_prueba)

	archivo_planilla = open(planilla_correciones, 'w')
	csv_planilla = csv.writer(archivo_planilla, delimiter='\t')
	csv_planilla.writerows(correcciones)
	archivo_planilla.close()

def csv_a_array(nombre_archivo_csv, a_partir_de_linea=0):
	with open(nombre_archivo_csv, 'r') as archivo_csv:
		archivo_csv = csv.reader(archivo_csv, delimiter='\t')
		return [linea for linea in archivo_csv][a_partir_de_linea:]


if __name__ == "__main__": 
	parser = argparse.ArgumentParser(description="Asigna una nota a los estudiantes y genera una planilla de salida.")
	parser.add_argument('respuestas_correctas', help='Respuestas correctas')
	parser.add_argument('respuestas_alumnos', help='Respuestas de los alumnos.')
	parser.add_argument('--planilla_correciones', help='Planilla de salida.')
	args = parser.parse_args()
	
	corregir(
		args.respuestas_correctas, 
		args.respuestas_alumnos, 
		args.planilla_correciones)