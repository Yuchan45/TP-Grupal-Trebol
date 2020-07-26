from generador_csv import *
from modulo_merge import *
from panel_general_funciones import *
from informacion_desarrollador import *
from consulta_funciones import *
from analizador_reutilizacion_codigo import *

def main():
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Genera fuente_unico y comentarios.csv. Y segun la opcion que tomes realizara la linea de ejecucion que corresponda.]
    """
    archivo = "programas.txt"
    lista_funciones, lista_comentarios = main_generador(archivo)
    main_modulo_merge(lista_funciones, lista_comentarios)
    print("Ya genere fuente_unico.csv y comentarios.csv!!!\n")

    print("(1) - Panel general de funciones")
    print("(2) - Consulta de funciones")
    print("(3) - Analizador de reutilizacion de codigo")
    print("(4) - Arbol de invocacion")
    print("(5) - Informacion por desarrollador")
    opcion = str(input("\nEscriba el numero de la opcion que quiere: "))

    if opcion == "1":
        print("\n")
        print("---PANEL GENERAL DE FUNCIONES ---------------------------------------------------------------------------------------------------------------------------------------------------------------")
        fuente_unico = open("fuente_unico.csv", "r")
        comentarios = open("comentarios.csv", "r")
        arch_salida = open("./salidas_modulos/panel_general.csv","w")
        main_panel_general_funciones(fuente_unico, comentarios, arch_salida)
        fuente_unico.close()
        comentarios.close()
        arch_salida.close()
    
    elif opcion == "2":
        print("\n")
        print("---CONSULTA DE FUNCIONES--------")
        comentarios = open("comentarios.csv", "r")
        fuente_unico = open("fuente_unico.csv", "r")
        salida = open("./salidas_modulos/ayuda_funciones.txt","w")
        lista_funciones = lista_de_funciones(fuente_unico)
        mostrar_cuadro(lista_funciones)
        main_consulta_funciones(fuente_unico, comentarios, salida, lista_funciones)
        comentarios.close()
        fuente_unico.close()
        salida.close()

    elif opcion == "3":
        fuente_unico = open("fuente_unico.csv", "r")
        salida = open("./salidas_modulos/analizador.txt","w")
        main_analizador(fuente_unico, salida)
        fuente_unico.close()
        salida.close()


    elif opcion == "5":
        print("\n")
        print("---INFORMACION POR DESARROLLADOR--------")
        fuente_unico = open("fuente_unico.csv", "r")
        comentarios = open("comentarios.csv", "r")
        arch_salida = open("./salidas_modulos/participacion.txt", "w")
        main_informacion_desarrollador(fuente_unico, comentarios, arch_salida)
        fuente_unico.close()
        comentarios.close()
        arch_salida.close()

main()