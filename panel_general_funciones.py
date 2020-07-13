linea_fuente = "mcd,'(nro_1, nro_2)', 'lib_matematica.py', 'break ', 'if abs(nro_1) < abs(nro_2):', 'menor = abs(nro_1)', 'mayor = abs(nro_2)', 'else:', 'menor = abs(nro_2)', 'mayor = abs(nro_1)', '', 'devovler = -1', 'elif menor == 0:', 'devolver = mayor', 'dividendo = mayor', 'divisor = menor', 'resto = mayor % divisor', '', 'while resto != 0:', 'dividendo = divisor', 'divisor = resto', 'resto = dividendo % divisor', '', 'devolver = divisor', '', 'return devolver', ''"
linea_fuente2 = "capicuas,'(list_words)', '6-show-capicuas-ordered-unrepeated.py', 'len_lista = len(list_words)', 'for i in range(len_lista):', 'palabra = list_words[i].lower()', 'invertida = ""', 'for j in range(len(palabra)-1, -1, -1):', 'invertida += palabra[j]', 'if palabra == invertida:', 'lista_capicuas.append(palabra)', 'return lista_capicuas', ''"
linea_comentarios = "capicuas,'[Autor: Yuchan]', '[Ayuda: Arma una lista con las palabras capicuas]', 'asdas', 'asdasdasdasads'"
linea_comentarios2 = "mcd,'[Autor: Ana Garcia]', '[Ayuda: Calcula el MCD entre los dos numeros recibidos, utilizando el', 'metodo de Euclides. En caso de no existir MCD, devolverá -1.]', 'Si ambos iguales a 0 no es posible mcd', 'Implementacion del algoritmo de Euclides'"
linea_comentarios3 = "solicitar_valor,'[Autor: Juan Perez]', '[Ayuda: Solicitar el ingreso de un valor y devolverlo, asegurando que', 'estara entre el minimo y el maximo pasado por parametro]'"
linea_comentarios4 = "ordered_list,'[Autor: Sin autor]', '[Ayuda: Sin ayuda]', 'Ordena alfabeticamente', 'asdasd'"

def buscar_funcion_modulo(linea):
    # Lee lineas de fuente_unico
    lista = linea.split(",")
    for campo in lista:
        if ".py" in campo:
            devolver = lista[0] + campo.rstrip("'")
    return devolver.replace(" '", ".")

def gen_lista_linea_codigo(linea):
    # Recibe una linea de un archivo de fuente_unico abierto y devuelve una lista con la seccion de las lineas de codigo como campos.
    lista = linea.split(".py', ") # La lista[1] va a tener todo lo que le sigue al modulo, osea el codigo.
    lista_linea_codigo = lista[1].split(", ") # lista_linea_codigo va a ser una lista con todo lo que le sigue al campo de modulo. Osea codigo puro
    return lista_linea_codigo


def count_parametros(linea):
    # Lee lineas de fuente_unico
    lista = linea.split("'")
    devolver = lista[1].split(",")
    return len(devolver)

def count_lineas_codigo(linea):
    # Lee lineas de fuente_unico
    lista_sin_vacios = []  
    lista_linea_codigo = gen_lista_linea_codigo(linea)
    # Elimino los espacios en blanco. Creo una lista vacia y meto los campos no vacios.
    for campo in lista_linea_codigo:
        if campo != "''":
            lista_sin_vacios.append(campo)
    return len(lista_sin_vacios)


def count_ifs(linea):
    # Lee lineas de fuente_unico
    contador = 0
    lista_linea_codigo = gen_lista_linea_codigo(linea)
    for campo in lista_linea_codigo:
        if "if " in campo or "elif " in campo: # Al poner el espacio en blanco luego del if, me aseguro de que es una sentencia.
            contador += 1
    return contador


def count_palabra(linea, palabra_buscada):
    # Sirve para buscar while, for, return, break y exit
    # Recibe fuente_unico. Como segundo parametro (string), se le pasa la palabra a buscar. Retorna la cantidad de apariciones.
    buscar = palabra_buscada + " " # Se le agrega el espacio para asegurarnos de que lo que estamos buscando es una sentencia y no adentro de un print.
    contador = 0
    lista_linea_codigo = gen_lista_linea_codigo(linea)
    for campo in lista_linea_codigo:
        if buscar in campo: # Al poner el espacio en blanco luego del if, me aseguro de que es una sentencia.
            contador += 1
    return contador

def count_comentarios(linea):
    # Lee lineas de comentarios.csv
    lista = linea.split("]',")
    if len(lista) > 2:
        comentarios_extra = lista[2].split("',")
        devolver = len(comentarios_extra)
    else:
        devolver = 0
    return devolver
    
    
def hay_ayuda(linea):
    # Lee lineas de comentarios.csv
    # Se fija si en la linea esta la ayuda descripcion. Devuelve si o no.
    lista = linea.split(",")
    if lista[2] == " '[Ayuda: Sin ayuda]'":
        devolver = "NO"
    else:
        devolver = "SI"
    return devolver
    
def autor(linea):
    # Lee lineas de comentarios.csv
    # Se fija si en la linea esta el autor. Devuelve su nombre en caso de estar.
    lista = linea.split(",")
    return lista[1]
    
    
def escribir_panel_general(arch_salida, funcion, parametros, lineas, invocaciones, returns, ifs, fors, whiles, breaks, exits, coments, ayudas, autores):
    escribir = funcion + ", " + str(parametros) + ", " + str(lineas) + ", " + str(invocaciones)+ ", " + str(returns) + ", " + str(ifs) + ", " + str(fors) + ", " + str(whiles) + ", " + str(breaks) + ", " + str(exits) + ", " + str(coments) + ", " + ayudas + ", " + autores + "\n"
    arch_salida.write(escribir)
    
    
def count_invocaciones(fuente_unico):
    # Hay que abrir el file y contar las veces que aparece tal funcion.
    # Recorro una primera vez para crearme una lista con todas las funciones. Y luego vuelvo a recorrer el archivo por cada funcion que haya para contar cuantas invocaciones hay, guardandolas en un dic.
    # Retorno el par que me piden por parametro.
    l_funciones = []
    dic_contador = {}
    fuente_unico.seek(0)
    linea = fuente_unico.readline()
    while linea:
        splits = linea.split(",")
        l_funciones.append(splits[0])
        linea = fuente_unico.readline()

    for i in range(len(l_funciones)):
        fuente_unico.seek(0)
        linea = fuente_unico.readline()
        while linea:
            if (l_funciones[i] + "(") in linea:
                if l_funciones[i] in dic_contador:
                    dic_contador[l_funciones[i]] += 1
                else:
                    dic_contador[l_funciones[i]] = 0

            linea = fuente_unico.readline()
        if l_funciones[i] not in dic_contador:
            dic_contador[l_funciones[i]] = 0
            
    return dic_contador

def main_panel_general_funciones(fuente_unico, comentarios, arch_salida):
    # Recibe como entrada fuente_unico.csv, comentarios.csv y un archivo de salida ya abiertos.
    dic_invocaciones = count_invocaciones(fuente_unico)
    fuente_unico.seek(0)
    linea = fuente_unico.readline()
    linea_c = comentarios.readline()
    arch_salida.write("FUNCION, PARAMETROS, LINEAS, INVOCACIONES, RETURNS, IF, FOR, WHILE, BREAKS, EXITS, COMENTS, AYUDAS, AUTORES\n")
    print('{:^55}{:^10}{:^10}{:^10}{:^10}{:^10}{:^5}{:^10}{:^10}{:^10}{:^10}{:^10}{:^25}'.format("FUNCION", "Parámetros", "Líneas","Invoacaiones","Returns","If/elif","for","while","break","Exit","Coment","Ayuda", "Autor"))
    while linea: # Ambos archivos tienen la misma cantidad de lineas asi que van a terminar al mismo tiempo.
        l_funcion_actual = linea.split(",")
        funcion_actual = l_funcion_actual[0]
        escribir_panel_general(arch_salida, buscar_funcion_modulo(linea), count_parametros(linea), count_lineas_codigo(linea), dic_invocaciones[funcion_actual], count_palabra(linea, "return"), count_ifs(linea), count_palabra(linea, "for"), count_palabra(linea, "while"), count_palabra(linea, "break"), count_palabra(linea, "exit"), count_comentarios(linea_c), hay_ayuda(linea_c), autor(linea_c))
        print('{:^55}{:^10}{:^10}{:^10}{:^10}{:^10}{:^5}{:^10}{:^10}{:^10}{:^10}{:^10}{:^25}'.format(buscar_funcion_modulo(linea), count_parametros(linea), count_lineas_codigo(linea), dic_invocaciones[funcion_actual],count_palabra(linea, "return"),count_ifs(linea),count_palabra(linea, "for"),count_palabra(linea, "while"),count_palabra(linea, "break"),count_palabra(linea, "exit"),count_comentarios(linea_c),hay_ayuda(linea_c), autor(linea_c)))
        
        
        linea = fuente_unico.readline()
        linea_c = comentarios.readline()
    print("-------------------------------------------------------")
    print("\nGenere el panel general.csv")
    print("*Los datos han sido registrados en panel_general.csv, ubicado en la carpeta de salidas_modulos")


