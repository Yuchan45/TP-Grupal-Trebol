from generador_csv import *
from modulo_merge import *
from panel_general_funciones import *

archivo = "programas.txt"
lista_funciones, lista_comentarios = main_generador(archivo)
main_modulo_merge(lista_funciones, lista_comentarios)
print("Ya genere fuente_unico.csv y comentarios.csv!!!")

print("(1) - Panel general de funciones")
print("(2) - Consulta de funciones")
print("(3) - Analizador de reutilizacion de codigo")
print("(4) - Arbol de invocacion")
print("(5) - Informacion por desarrollador")
opcion = str(input("Escriba el numero de la opcion que quiere: "))

if opcion == "1":
    print("\n")
    print("PANEL GENERAL DE FUNCIONES")
    fuente_unico = open("fuente_unico.csv", "r")
    comentarios = open("comentarios.csv", "r")
    arch_salida = open("./salidas_modulos/panel_general.csv","w")
    main_panel_general_funciones(fuente_unico, comentarios, arch_salida)
    fuente_unico.close()
    comentarios.close()
    arch_salida.close()
