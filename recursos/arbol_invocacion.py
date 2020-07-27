def carga_dic_invocaciones(fuente_unico, lista_funciones):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y una lista con todas las funciones que hay. Devuelve un diccionario con clave: nombre de la funcion y de valor una lista con las funciones que invoca.]
    """
    dic_invocaciones = {}
    lista_agregar = []
    linea = fuente_unico.readline()
    while linea:
        aux = linea.split(",")
        n_funcion_dic = aux[0]
        lista_agregar = lista_invocaciones(linea, lista_funciones)
        dic_invocaciones[n_funcion_dic] = lista_agregar
        linea = fuente_unico.readline()
    return dic_invocaciones 
    
    
def carga_lista_funciones(fuente_unico):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve una lista con las funciones que hay en ella.]
    """
    lista_funciones = []
    linea = fuente_unico.readline()
    while linea:
        funcion = linea.split(",")
        lista_funciones.append(funcion[0])
        linea = fuente_unico.readline()
    return lista_funciones


def lista_invocaciones(linea, lista_funciones):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea y una lista con las funciones q pueden aparecer, y te arma una lista con las funciones q aparecen en la linea. Devuelve dicha lista.]
    """
    lista_agregar = []
    for funcion in lista_funciones:
        if funcion + "(" in linea:
            lista_agregar.append(funcion)
    return lista_agregar

def gen_lista_lineas(linea):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve una lista con la seccion de las lineas de codigo como campos.]
    """
    linea = linea.rstrip("\n")
    lista = linea.split(".py', ") # La lista[1] va a tener todo lo que le sigue al modulo, osea el codigo.
    lista_linea_codigo = lista[1].split("', ") # lista_linea_codigo va a ser una lista con todo lo que le sigue al campo de modulo. Osea codigo puro
    return lista_linea_codigo

def contador_lineas(linea):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve la cantidad de lineas de codigo que hay en la funcion de esa linea.]
    """
    lista_sin_vacios = []  
    lista_linea_codigo = gen_lista_lineas(linea)
    # Elimino los espacios en blanco. Creo una lista vacia y meto los campos no vacios.
    for campo in lista_linea_codigo:
        if campo != "''" and campo != "'":
            lista_sin_vacios.append(campo)
    return len(lista_sin_vacios)


def load_dic_lineas_codigo(fuente_unico):
    """[Autor: Yuchan]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve un diccionario con funcion como clave y cantidad de lineas como valor.]
    """
    dic_lineas_codigo = {}
    linea = fuente_unico.readline()
    while linea:
        aux = linea.split(",")
        funcion = aux[0]
        lineas = contador_lineas(linea)
        dic_lineas_codigo[funcion] = lineas
        linea = fuente_unico.readline()
    return dic_lineas_codigo

def hacer_cadena_invocaciones(dic, funcion, cadena, nivel, dic_lineas_codigo, lista_cadena):
    """[Autor: Yuchan]
       [Ayuda: Recibe un dic con key funciones y de valor, una lista con las funciones a las que llama, una lista de las funciones q llama, recibe una funcion "BASE" y finalmente recibe "cadena" que es una lista a la que se agregaran las lineas a imprimir y un dic con la cantidad de lineas por funcion. (No la puedo poner adentro de la funcion xq como es recursiva, se va a borrar). Imprime un arbol de invocaciones.]
    """
    # El parametro lista_cadena es una lista que tiene listas que tienen las lineas a imprimir. La cree para luego ahcer que todas las listas anidadas tengan el mismo len, y asi poder crear un format con n parametros. Pero no me salio.
    nivel += 1
    # Uso las variables "nivel" para saber en que ciclo de la funcion estoy. Esto lo uso luego para saber con cuantos espacios en blanco rellenar al principio del array con las cadenas a imprimir y que quede ordenado.
    if len(dic[funcion]) != 0 and dic[funcion] != funcion:
        for i in dic[funcion]:
            # lineas es = "(x cant lineas)"
            lineas = " (" + str(dic_lineas_codigo[i]) + ") "
            cadena.append( i + lineas)
            # Vuelvo a ciclar (recursividad) hasta que no entre en la condicion
            hacer_cadena_invocaciones(dic, i, cadena, nivel, dic_lineas_codigo, lista_cadena)
    else:
        # Entra aca cuando la funcion ya no llama a otra funcion. Osea que termina.
        # Agrego los espacios en blanco al comienzo del array, dependiendo de cuantos ciclos ya realizo la funcion (nivel). Si es nivel 2, se agregan 2 espacion en blanco al comienzo de la lista.
        if len(cadena) < 5:
            espacios_agregar = nivel - len(cadena)
            for i in range(espacios_agregar):
                cadena.insert(i, "")
        print(" ---> ".join(cadena))
        lista_cadena.append(cadena)
        nivel = 0
        cadena.clear()
    
def main_arbol_invocacion(dic, dic_lineas_codigo):
    """[Autor: Yuchan]
       [Ayuda: Recibe un dic funcion: lista de funciones invocadas y un diccionario funcion: cantidad lineas de codigo. Ejecuta una funcion recursiva la cual se encarga de imprimir por pantalla.]
    """
    cadena = []
    lista_cadena = []
    for funcion in dic.keys():
        if "main_main" in funcion:
            flag = True
            print(funcion + "\n")
            nivel = 0
            cadena.append(funcion)
            hacer_cadena_invocaciones(dic, funcion, cadena, nivel, dic_lineas_codigo, lista_cadena)
            #print(lista_cadena)
            print("\n---------------------")
            

fuente_unico = open("fuente_unico.csv", "r")
lista_funciones = carga_lista_funciones(fuente_unico)
fuente_unico.seek(0)

dic_lineas_codigo = load_dic_lineas_codigo(fuente_unico)
fuente_unico.seek(0)

diccionario_invocaciones = carga_dic_invocaciones(fuente_unico, lista_funciones)
main_arbol_invocacion(diccionario_invocaciones, dic_lineas_codigo)
print(diccionario_invocaciones)
    
fuente_unico.close()






