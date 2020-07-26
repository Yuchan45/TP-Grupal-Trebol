def lista_invocaciones_id(linea, lista_funciones, dic_funcion_id):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe una linea, una lista con las funciones q pueden aparecer y el diccionario_id_funcion. Te arma una lista con los ID de las funciones q aparecen en la linea. Devuelve dicha lista.]
    """
    lista_agregar = []
    for funcion in lista_funciones:
        if funcion + "(" in linea:
            add = dic_funcion_id[funcion] # Aca me guardo el id de la funcion
            lista_agregar.append(add)
    return lista_agregar


def carga_lista_funciones(fuente_unico):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve una lista con las funciones que hay en ella.]
    """
    lista_funciones = []
    linea = fuente_unico.readline()
    while linea:
        funcion = linea.split(",")
        lista_funciones.append(funcion[0])
        linea = fuente_unico.readline()
    fuente_unico.seek(0) # Dejo el puntero de fuente_unico en 0 xq luego lo puedo volver a usar.
    return lista_funciones


def gen_dic_funcion_id(lista_funciones):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe la lista de funciones y la hace diccionario, asignandole como key la funcion/nombre y de valor su orden (id).]
    """
    dic_funcion_id = {}
    for i in range(len(lista_funciones)):
        dic_funcion_id[lista_funciones[i]] = i + 1
    return dic_funcion_id


def gen_dic_inv_x(fuente_unico, lista_funciones, dic_funcion_id):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y una lista con todas las funciones que hay. Devuelve un diccionario con clave: nombre de la funcion y de valor una lista con los ID de las funciones a las que llama (PUEDE HABER IDS REPETIDAS).]
    """
    dic_invocaciones = {}
    lista_agregar = []

    linea = fuente_unico.readline()
    while linea:
        aux = linea.split(",")
        n_funcion_dic = aux[0]
        # La funcion lista_invocaciones me devuelve una lista con los ID de las funciones que aparecen en la linea que estoy leyendo ahora.
        lista_agregar = lista_invocaciones_id(linea, lista_funciones, dic_funcion_id)
        # Le agrego la lista al diccionario con su funcion correspondiente.
        dic_invocaciones[n_funcion_dic] = lista_agregar
        linea = fuente_unico.readline()
    fuente_unico.seek(0) # Dejo el puntero de fuente_unico en 0 xq luego lo puedo volver a usar.
    return dic_invocaciones


def lista_invoc_count(dic_inv_x, funcion):
    """[Autor: Fabiola Siles]
       [Ayuda: Recorro el dic_inv_x, el cual tiene una lista con los ID de las funciones invocadas (puede tener ids repetidas). Y cuenta las repeticiones de los id (que serian la cantidad de veces que se la invoca). Genero una lista de tuplas asi: [(id funcion, nro repeticiones), (..., ...)].]
    """
    lista_agregar = []
    
    for i in range(len(dic_inv_x)):
        count = dic_inv_x[funcion].count(i)
        if count > 0 and count < 100:
            lista_agregar.append((i, count))
    return lista_agregar


def gen_dic_invoc_count(fuente_unico, lista_funciones, dic_funcion_id, dic_inv_x):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y una lista con todas las funciones que hay. Devuelve un diccionario con clave: nombre de la funcion y de valor una lista de tuplas de este estilo. "funcion" : [(id funcion, repeticiones ), (..., ...)].]
    """
    dic_invoc_count = {}
    lista_agregar = []

    linea = fuente_unico.readline()
    while linea:
        aux = linea.split(",")
        n_funcion_dic = aux[0]
        # La funcion lista_invocaciones me devuelve una lista con los ID de las funciones que aparecen en la linea que estoy leyendo ahora.
        lista_agregar = lista_invoc_count(dic_inv_x, n_funcion_dic) # Haciendo uso de un diccionario ya creado previamente (dic_inv_x, el cual es asi: "main" : [5, 5, 12, 18]), recorro sus valores y cuento la cantidad de repeticiones. Asi me creo una lista de tuplas con [(id funcion, repeticion), ()] .
        # Le agrego la lista de tuplas al diccionario con su funcion correspondiente.
        dic_invoc_count[n_funcion_dic] = lista_agregar
        linea = fuente_unico.readline()
    fuente_unico.seek(0) # Dejo el puntero de fuente_unico en 0 xq luego lo puedo volver a usar.
    return dic_invoc_count


def cargar_matriz(dic_invoc_count, matriz):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe el diccionario de funcion y lista de tuplas(id_funcion, repeticiones). Y tambien recibe una matriz ya creada con espacios vacios y con un ancho y largo correspondiente a la cantidad de funciones. Devuelve la matriz cargada con los datos del diccionario.]
    """
    x = 0
    for i in dic_invoc_count.keys():

        lista_tuplas = dic_invoc_count[i] # Me agarro la lista de tuplas (id funcion, repeticiones) del diccionario.
        for tupla in lista_tuplas:
            # Recorro la lista de tuplas y le asigno a la matriz el valor correspondiente. Si la tupla es (5, 3) y la fila "x" es = 0, lo que hago es poner en la matriz[0][5] el valor 3(cant repeticiones).
            matriz[x][tupla[0]] = str(tupla[1])
            # Como los "numeros" en la tabla indican la cantidad de veces que se invoca a la funcion de la columna y las cruces "X" indican que la funcion de la fila es invocada por la funcion de la columna, se trata de una matriz simetrica.
            # Asi que intercambio "x" e "y" en la matriz y le asigno a la matriz una "X".
            matriz[tupla[0]][x] = "X"

        x += 1 # Sumo 1 a "x" para que avance a la siguente fila.
    return matriz


def gen_ultima_fila(matriz):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe una matriz con solo numeros(int) y calcula la sumatoria de sus columnas, generando una lista con los resultados de cada columna.]
    """
    ultima_fila = []
    columnas = len(matriz)
    for j in range(columnas):
        # fila[j] seria (en caso de que sea la primer iteracion del for) el primer valor de la fila. Juntando todos los primeros valores de las filas, me hago la primer columna.
        suma = sum([ int(fila[j]) for fila in matriz if fila[j] not in [" ", "X"] ])
        ultima_fila.append(suma)
    return ultima_fila

def imprimir_todo(tamaño, dic_funcion_id, matriz, ultima_fila):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe el tamaño (cantidad de funciones), diccionario funcion_id, la matriz cargada con todos los datos, la ultima fila a agregar y el archivo de salida. Realiza el proceso de ejecucion para imprimir por pantalla lo solicitado en el enunciado.]
    """
    imprimir_cabecera(tamaño)
    imprimir_lineas(dic_funcion_id, matriz)
    imprimir_ultima_fila(ultima_fila, tamaño)
    
    
def imprimir_cabecera(largo):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe el largo, osea la cantidad de columnas que tiene que generar. Haciendo uso del format, imprime la cabecera de la tabla.]
    """
    print('{:^35}'.format("FUNCIONES"), end = "")
    for i in range(1, largo+1):
        if i < 10:
            num = "0" + str(i)
        else:
            num = str(i)
        print('{:^3}'.format(str(num)), end="")
    print("\n")

def imprimir_lineas(dic_funcion_id, matriz):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe el diccionario funcion_id, el tamaño (cantidad de funciones) y la matriz cargada con todos los datos. Imprime por pantalla el cuerpo.]
    """
    x = 0
    for funcion in dic_funcion_id:
        print('{:<35}'.format(str(dic_funcion_id[funcion]) + " - " + str(funcion)), end = "")
        for y in range(0, len(dic_funcion_id)):
            print('{:^3}'.format(str(matriz[x][y])), end="")
        x += 1 
        print("\n")


def imprimir_ultima_fila(ultima_fila, tamaño):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe la ultima fila a imprimir y el tamaño (cantidad de funciones). Imprime por pantalla la ultima linea.]
    """
    print('{:<35}'.format("Total invocaciones"), end = "")
    for i in range(0, tamaño):
            print('{:^3}'.format(str(ultima_fila[i])), end="")
            
            
def crear_matriz(ancho, alto):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe el ancho y el alto de la matriz a generar. Crea una matriz de w, h de altura y ancho. La lleno con espacios vacios.]
    """
    w, h = ancho, alto;
    matriz = [[" " for x in range(w)] for y in range(h)]
    return matriz
 
    
def escribir_analizador(tamaño, dic_funcion_id, matriz, ultima_fila, salida):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe el tamaño (cantidad de funciones), diccionario funcion_id, la matriz cargada con todos los datos, la ultima fila a agregar y el archivo de salida. Realiza el proceso de ejecucion para generar analizador.txt.]
    """
    escribir_cabecera(salida, tamaño)
    escribir_cuerpo(salida, dic_funcion_id, tamaño, matriz)
    escribir_ultima_fila(salida, ultima_fila, tamaño)
    print("\n\n*Genere el archivo analizador.txt el cual se encuentra ubicado en la carpeta 'salidas_modulos'.")

def escribir_cabecera(salida, tamaño):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe la salida y el tamaño (cantidad de funciones). Escribe la cabecera en el analizador.txt.]
    """
    salida.write('{:^35}'.format("FUNCIONES"))
    for i in range(1, tamaño+1):
        if i < 10:
            num = "0" + str(i)
        else:
            num = str(i)
        salida.write('{:^3}'.format(str(num)))
    salida.write("\n")
    
def escribir_cuerpo(salida, dic_funcion_id, tamaño, matriz):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe el diccionario funcion_id, el tamaño (cantidad de funciones) y la matriz cargada con todos los datos. Escribe en el analizador.txt el cuerpo.]
    """
    x = 0
    for funcion in dic_funcion_id:
        salida.write('{:<35}'.format(str(dic_funcion_id[funcion]) + " - " + str(funcion)))
        for y in range(0, tamaño):
            salida.write('{:^3}'.format(str(matriz[x][y])))
        x += 1 
        salida.write("\n")

def escribir_ultima_fila(salida, ultima_fila, tamaño):
    """[Autor: Fabiola Siles]
       [Ayuda: Recibe la ultima fila a escribir y el tamaño (cantidad de funciones). Escribe en el analizador.txt la ultima linea.]
    """
    salida.write('{:<35}'.format("Total invocaciones"))
    for i in range(0, tamaño):
            salida.write('{:^3}'.format(str(ultima_fila[i])))

def main_analizador(fuente_unico, salida):
    """[Autor: Fabiola Siles]
       [Ayuda: Realiza la linea de ejecucion a fin de cumplir con lo solicitado en el enunciado.]
    """
    lista_funciones = carga_lista_funciones(fuente_unico)
    dic_funcion_id = gen_dic_funcion_id(lista_funciones)
    dic_inv_x = gen_dic_inv_x(fuente_unico, lista_funciones, dic_funcion_id)
    dic_invoc_count = gen_dic_invoc_count(fuente_unico, lista_funciones, dic_funcion_id, dic_inv_x)
    # Ya genere todos los diccionarios que voy a necesitar para creame la matriz.
    tamaño = len(dic_funcion_id)
    matriz = crear_matriz(tamaño, tamaño)
    matriz_cargada = cargar_matriz(dic_invoc_count, matriz)
    ultima_fila = gen_ultima_fila(matriz)
    # Imprimo y genero el analizador.txt
    imprimir_todo(tamaño, dic_funcion_id, matriz_cargada, ultima_fila)    
    escribir_analizador(tamaño, dic_funcion_id, matriz_cargada, ultima_fila, salida)

