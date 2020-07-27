import re
import os

palabra_func = "^def (\w+)" 
dict_funciones = {}
dict_comentarios = {}
comentario_multiple = chr(34) + chr(34) + chr(34)
comentario_simple = chr(35) 


def leer_linea(archivo):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe un archivo abierto y devuelve la linea]
    """
    linea = archivo.readline()
    return linea

    
def encontrar_llave_param(linea):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea y retorna el nombre de la funcion y parametros]
    """
    aux = linea.split(" ", 1)
    aux2 = aux[1].split("(", 1)
    key = aux2[0]
    param = "(" + aux2[1].rstrip(":\n")
    return key, param


def generar_dict_funciones(codigo):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe un archivo abierto con codigo y genera un diccionario con solo codigo, cuyas claves seran los nombres de las funciones]
    """
    linea = leer_linea(codigo)
    while linea:
        nom_funcion = re.search(palabra_func, linea)
        if nom_funcion:
            key, parametros = encontrar_llave_param(linea)
            dict_funciones[key] = [parametros, os.path.basename(codigo.name)]
            linea = leer_linea(codigo)
            while re.match(r'\s', linea):
                # Esto lo intente meter en una funcion pero el problema era que cuando hacia el skip en la funcion, no se mantenia el index de la linea en el bloque principal.
                if comentario_multiple in linea: 
                    linea = leer_linea(codigo)
                    while not comentario_multiple in linea:
                        linea = leer_linea(codigo)
                    linea = leer_linea(codigo)
                elif comentario_simple in linea:
                    linea = linea.lstrip(" ")
                    l_split = linea.split("#")
                    if l_split[0] != "''":
                        dict_funciones[key].append(l_split[0])
                        linea = leer_linea(codigo)
                    else:
                        linea = leer_linea(codigo)
                else:
                    dict_funciones[key].append(linea.strip(" ").rstrip("\n"))
                    linea = leer_linea(codigo)
        else:
            # Si es una linea que no pertenece a un funcion, pasa a la sig linea. (la guarda en el dict_extra del cual se generara extra.csv)
            linea = leer_linea(codigo)           
    return dict_funciones


def buscar_autor(lista_comentarios):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una lista con comentarios y devuelve el autor en caso de existir]
    """
    autor = 0
    for k in range(len(lista_comentarios)):
        if "autor:" in lista_comentarios[k].lower():
            devolver = lista_comentarios[k].lstrip(" ").rstrip("\n").lstrip(comentario_multiple)
            autor += 1
    if autor < 1:
        devolver = "[Autor: Sin autor]"
    return devolver

            
def buscar_ayuda(lista_comentarios):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una lista de comentarios y devuleve la ayuda en caso de existir]
    """
    ayuda = 0
    for j in range(len(lista_comentarios)):
        if "ayuda" in lista_comentarios[j].lower():
            devolver = lista_comentarios[j].lstrip(" ").rstrip("\n")
            ayuda += 1
    if ayuda < 1:
        devolver = "[Ayuda: Sin ayuda]"
    return devolver


def otros_coments(lista_comentarios):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una lista de comentarios y devuleve los comentarios que no son ni ayuda ni de autor]
    """
    lista_coments = []
    for h in range(len(lista_comentarios)):
        if not "autor" in lista_comentarios[h].lower() and not "ayuda" in lista_comentarios[h].lower() and lista_comentarios[h].lstrip(" ").rstrip("\n") != comentario_multiple:
            lista_coments.append(lista_comentarios[h].lstrip(" ").rstrip("\n"))
    return lista_coments
            
def cargar_dic_coment(key, autor, ayuda, otros):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe el nombre de la funcion, el autor, ayuda y comentarios extra, y los agrega al diccionario de comentarios]
    """
    dict_comentarios[key] = [autor, ayuda]
    dict_comentarios[key].extend(otros)

def generar_dict_comentarios(codigo):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe un archivo abierto con codigo y genera un diccionario con solo comentarios, cuyas claves seran los nombres de las funciones.]
    """
    lista_comentarios = []
    linea = leer_linea(codigo)
    while linea:
        nom_funcion = re.search(palabra_func, linea)
        if nom_funcion:
            key, parametros = encontrar_llave_param(linea)
            linea = leer_linea(codigo)
            # Mientras no encuentre una linea sin "tab" al comienzo...
            while re.match(r'\s', linea): 
                if comentario_multiple in linea:
                    lista_comentarios.append(linea)
                    linea = leer_linea(codigo)
                    while not comentario_multiple in linea:
                        lista_comentarios.append(linea)
                        linea = leer_linea(codigo)
                    linea = leer_linea(codigo)
                elif comentario_simple in linea:
                    agregar = linea.split("#") # HACER QUE GUARDE EN LA LISTA LA LINEA A PARTIR DEL #
                    lista_comentarios.append(agregar[1].rstrip("\n"))
                    linea = leer_linea(codigo)
                else:
                    linea = leer_linea(codigo)
            cargar_dic_coment(key, buscar_autor(lista_comentarios), buscar_ayuda(lista_comentarios), otros_coments(lista_comentarios))
            lista_comentarios.clear()
        else:
            linea = leer_linea(codigo)
    lista_comentarios.clear()
    return dict_comentarios


def ordenar_dict(diccionario):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe un diccionario y lo ordena alfabeticamente por key. Retorna un diccionario. Casteando el "dict" logro que me retorne un diccionario y no una lista de tuplas]
    """
    dic_ordenado = dict(sorted(diccionario.items()))
    return dic_ordenado


def escribir_registros(archivo, diccionario):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe un archivo abierto(en donde escribir) y un diccionario. Escribe el dic en el archivo.]
    """
    for key in diccionario:
        registros = str(diccionario[key]).rstrip("]").lstrip("[")
        linea = key + "," + registros + "\n"
        archivo.write(linea)
  
def crear_funciones_csv(linea, codigo, l_fun):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea, codigo que es un archivo abierto y una lista a la que se le van agregando paths de los modulos con funciones (que luego se usara para el merge). Realiza la linea de ejecucion a fin de crear los funciones.csv]
    """
    dict_funciones = generar_dict_funciones(codigo)
    dict_funciones_ordenado = ordenar_dict(dict_funciones)
    ruta_csv_funciones = "./salidas/csv_funciones_" + os.path.basename(codigo.name).rstrip(".py") + ".csv"
    
    guardar = open(ruta_csv_funciones, "w")
    escribir_registros(guardar, dict_funciones_ordenado)
    guardar.close()  
    l_fun.append(ruta_csv_funciones) # Esta es la lista que se devuelve luego. Tiene todas las funciones.

    codigo.seek(0)
        
def crear_comentarios_csv(linea, codigo, l_com):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea, codigo que es un archivo abierto y una lista a la que se le van agregando paths de los modulos con comentarios (que luego se usara para el merge). Realiza la linea de ejecucion a fin de crear los comentarios.csv]
    """
    dict_comentarios = generar_dict_comentarios(codigo)
    dict_comentarios_ordenado = ordenar_dict(dict_comentarios)
    ruta_csv_comentarios = "./salidas/csv_comentarios_" + os.path.basename(codigo.name).rstrip(".py") + ".csv"
    guardar = open(ruta_csv_comentarios, "w")
    escribir_registros(guardar, dict_comentarios_ordenado)
    guardar.close()
    l_com.append(ruta_csv_comentarios) # Esta es la lista que se devuelve luego. Tiene una lista con los comentarios.
        
def main_generador(archivo):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe el txt con las path de los archivos a analizar y genera un csv comentario y un csv funciones por cada archivo. Devuelve una lista con las funciones y una lista con comentarios]
    """
    l_fun = []
    l_com = []
    programas = open(archivo, "r")
    l_fun.clear() # Hago esto porque es probable que esto se haga varias veces, asi que hay q limpiar la lista para que no se repitan datos.
    l_com.clear()
    linea = leer_linea(programas)
    while linea:
        ruta = linea.rstrip("\n")
        codigo = open(ruta, "r")
        
        crear_funciones_csv(linea, codigo, l_fun)

        crear_comentarios_csv(linea, codigo, l_com)

        codigo.close()
        
        dict_funciones.clear() # Hago esto porque es probable que esto se haga varias veces, asi que hay q limpiar la lista para que no se repitan datos.
        dict_comentarios.clear()

        linea = leer_linea(programas)
    return l_fun, l_com # Estas se usaran luego en el modulo_merge para abrir los archivos correspondientes a mergear.
        



