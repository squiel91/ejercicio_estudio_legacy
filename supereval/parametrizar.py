import argparse
from supereval.parametrizar import parametrizar_eval

parser = argparse.ArgumentParser(description="Crea prueba a partir de los ejercicios parametrizados")
parser.add_argument('titulo', help='Titulo de la prueba')
parser.add_argument('ejercicios_parametrizados', nargs='+', 
					help='Lista de ejercicios parametrizados.')
parser.add_argument('--cantidad', type=int, help='Cantidad de pruebas')
parser.add_argument('--texto', action="store_true", help='Exportacion a texto plano')
parser.add_argument('--pdf', action="store_true", help='Exportacion a PDF')
parser.add_argument('--eva', action="store_true", help='Para importar a entorno EVA')
args = parser.parse_args()

print("Parametrizando evaluacion ...")
parametrizar_eval(
	args.titulo, 
	args.ejercicios_parametrizados, 
	numero_instancias=args.cantidad or 10, 
	texto=args.texto, 
	eva=args.eva, 
	latex=args.pdf)

print("Finalizado.")

