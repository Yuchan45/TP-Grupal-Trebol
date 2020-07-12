from generador_csv import *
from modulo_merge import *

archivo = "programas.txt"
lista_funciones, lista_comentarios = main_generador(archivo)
print("Termine de generar los csvs.")
main_modulo_merge(lista_funciones, lista_comentarios)
print("Termine de mergear y generar fuente_unico.csv y comentarios.csv")
