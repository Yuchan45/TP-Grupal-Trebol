#from panel_general_funciones import *
def buscar_dueño(linea):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de un archivo de comentarios.csv o fuente_unico.csv abierto y devuelve el primer campo. Osea el autor.]
    """
    lista = linea.split(",")
    return lista[1]

def buscar_funcion(linea):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de comentarios.csv por parametro y devuelve el nombre de la funcion]
    """
    lista = linea.split(",")
    return lista[0]


def gen_lista_linea_codigo(linea):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve una lista con la seccion de las lineas de codigo como campos.]
    """
    linea = linea.rstrip("\n")
    lista = linea.split(".py', ") # La lista[1] va a tener todo lo que le sigue al modulo, osea el codigo.
    lista_linea_codigo = lista[1].split("', ") # lista_linea_codigo va a ser una lista con todo lo que le sigue al campo de modulo. Osea codigo puro
    #print(lista_linea_codigo)
    return lista_linea_codigo


def count_lineas_codigo(linea):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve la cantidad de lineas de codigo que hay en la funcion de esa linea.]
    """
    lista_sin_vacios = []  
    lista_linea_codigo = gen_lista_linea_codigo(linea)
    # Elimino los espacios en blanco. Creo una lista vacia y meto los campos no vacios.
    for campo in lista_linea_codigo:
        if campo != "''" and campo != "'":
            lista_sin_vacios.append(campo)
    #print(lista_sin_vacios)
    return len(lista_sin_vacios)


def carga_dic_participacion(fuente_unico, comentarios):
    """[Autor: Yuchan]
       [Ayuda: Recibe el archivo fuente_unico y comentarios.csv abierto, y devuelve un diccionario anidado de la sigiente forma: {dic = { "'[Autor : Yuchan]'": {'capicuas': 12,'delete_repeated': 7},] }. ]
    """
    dic_participacion = {}
    linea = fuente_unico.readline()
    linea_c = comentarios.readline()
    while linea:
        # Ambos archivos tienen la misma cantidad de lineas asi que van a terminar al mismo tiempo.
        au = buscar_dueño(linea_c).lstrip("'").rstrip("'")
        funcion = buscar_funcion(linea)
        cant_lineas = count_lineas_codigo(linea)
        #print(au, funcion, cant_lineas)
        if au not in dic_participacion:
            dic_participacion[au] = {funcion: cant_lineas}
        else:
            dic_participacion[au].update({funcion: cant_lineas})   
        linea = fuente_unico.readline()
        linea_c = comentarios.readline()
    return dic_participacion
        
def calc_total_lineas(dic_participacion):
    """[Autor: Yuchan]
       [Ayuda: Recibe un diccionario anidado con claves(autores) y subclaves(nombres de funcion). Devuelve el acumulador del total de lineas.]
    """
    total_lineas = 0
    for autor in dic_participacion:
        # Casteandole el dict al sorted, logro que me devuelva un dic y no una lista de tuplas.
        dic_part_ord = dict(sorted(dic_participacion[autor].items(), key=lambda item: item[1], reverse=True))
        for funcion in dic_part_ord:
            total_lineas += dic_part_ord[funcion]
    return total_lineas

def calc_porcentaje(total_lineas, lineas_funcion):
    """[Autor: Yuchan]
       [Ayuda: Recibe el total de lineas y las lineas por funcion. Devuelve el promedio.]
    """
    porcentaje = 0
    porcentaje = int(round((lineas_funcion * 100) / total_lineas, 0))
    return porcentaje

def imprimir_info_desarrollador(total_lineas, dic_participacion):
    """[Autor: Yuchan]
       [Ayuda: Recibe el total de lineas en todo el codigo y un diccionario(cargado mediante la funcion carga_dic_part) e imprime los datos del diccionario por pantalla.]
    """
    contador = 0
    print("Informe de Desarrolo Por Autor \n")
    for autor in dic_participacion:
        print(autor)
        print('{:^30}{:^10}'.format("FUNCION", "Líneas"))
        print('{:^30}{:^10}'.format("-----------------------------", "----------"))
        dic_part_ord = dict(sorted(dic_participacion[autor].items(), key=lambda item: item[1], reverse=True))
        for funcion in dic_part_ord:
            print('{:^30}{:^10}'.format(funcion, dic_part_ord[funcion]))
            contador += dic_part_ord[funcion]
        print("\n")
        porcentaje = calc_porcentaje(total_lineas, contador)
        print('{:^30}{:^10}{:^10}'.format(str(len(dic_part_ord)) + " Funciones - Lineas", contador, str(porcentaje) + "%"))   
        contador = 0
        print('{:^30}{:^10}'.format("-----------------------------", "----------"))
        print("\n")
    
def escribir_info_desarrollador(arch_salida, total_lineas, dic_participacion):
    """[Autor: Yuchan]
       [Ayuda: Recibe el archivo de salida, el total de lineas en todo el codigo y un diccionario(cargado mediante la funcion carga_dic_part). Escribe los datos del diccionario en el archivo de salida.]
    """
    contador = 0
    arch_salida.write("Informe de Desarrollo Por Autor \n")
    for autor in dic_participacion:
        arch_salida.write(autor + "\n")
        arch_salida.write('{:^30}{:^10}'.format("FUNCION", "Líneas") + "\n")   
        arch_salida.write('{:^30}{:^10}'.format("-----------------------------", "----------") + "\n")
        dic_part_ord = dict(sorted(dic_participacion[autor].items(), key=lambda item: item[1], reverse=True))
        for funcion in dic_part_ord:
            arch_salida.write('{:^30}{:^10}'.format(funcion, dic_part_ord[funcion]) + "\n")
            contador += dic_part_ord[funcion]
        arch_salida.write("\n")
        porcentaje = calc_porcentaje(total_lineas, contador)
        arch_salida.write('{:^30}{:^10}{:^10}'.format(str(len(dic_part_ord)) + " Funciones - Lineas", contador, str(porcentaje) + "%") + "\n")   
        contador = 0
        arch_salida.write('{:^30}{:^10}'.format("-----------------------------", "----------") + "\n")
        arch_salida.write("\n")


def main_informacion_desarrollador(fuente_unico, comentarios, salida):
    """[Autor: Yuchan]
       [Ayuda: Recibe fuente_unico.csv, comentarios.csv y un archivo de salida. Realiza la cadena de ejecucion a fin de cumplir con el enunciado utilizando las diferentes funciones del modulo.]
    """
    dic_participacion = carga_dic_participacion(fuente_unico, comentarios)
    total_lineas = calc_total_lineas(dic_participacion)
    imprimir_info_desarrollador(total_lineas, dic_participacion)
    escribir_info_desarrollador(salida, total_lineas, dic_participacion)
    print("*Genere el participacion.txt, ubicado en la carpeta de salidas_modulos")

      
        