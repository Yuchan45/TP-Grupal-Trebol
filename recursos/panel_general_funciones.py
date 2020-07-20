def buscar_funcion_modulo(linea):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de fuente_unico.csv por parametro y devuelve el nombre de la funcion, concatenado con el modulo al que pertenece]
    """
    lista = linea.split(",")
    for campo in lista:
        if ".py'" in campo:
            devolver = lista[0] + campo.rstrip("'")
    return devolver.replace(" '", ".")

def gen_lista_linea_codigo(linea):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve una lista con la seccion de las lineas de codigo como campos.]
    """
    linea = linea.rstrip("\n")
    lista = linea.split(".py', ") # La lista[1] va a tener todo lo que le sigue al modulo, osea el codigo.
    lista_linea_codigo = lista[1].split("', ") # lista_linea_codigo va a ser una lista con todo lo que le sigue al campo de modulo. Osea codigo puro
    return lista_linea_codigo


def count_parametros(linea):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve la cantidad de paramtros que recibe la funcion.]
    """
    lista = linea.split("'")
    devolver = lista[1].split(",")
    return len(devolver)

def count_lineas_codigo(linea):
    """[Autor: Tomas Yu Nakasone]
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


def count_ifs(linea):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y devuelve la cantidad de ifs/elifs.]
    """
    contador = 0
    lista_linea_codigo = gen_lista_linea_codigo(linea)
    for campo in lista_linea_codigo:
        # Al poner el espacio en blanco luego del if, me aseguro de que es una sentencia.
        if "if " in campo or "elif " in campo: 
            contador += 1
    return contador


def count_palabra(linea, palabra_buscada):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de un archivo de fuente_unico abierto y un string el cual es la palabra a buscar en la linea. Devuelve la cantidad de apariciones de la palabra buscada.]
    """
    # Sirve para buscar while, for, return, break y exit
    buscar = palabra_buscada + " " # Se le agrega el espacio para asegurarnos de que lo que estamos buscando es una sentencia y no adentro de un print.
    contador = 0
    lista_linea_codigo = gen_lista_linea_codigo(linea)
    for campo in lista_linea_codigo:
        if buscar in campo: 
            contador += 1
    return contador

def count_comentarios(linea):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de un archivo de comentarios.csv abierto y devuelve la cantidad de comentarios(EXTRA DESCRIPCION).]
    """
    lista = linea.split("]',")
    # Las ayudas y autores estan definidos entre " [ ] ".
    if len(lista) > 2:
        comentarios_extra = lista[2].split("',")
        devolver = len(comentarios_extra)
    else:
        devolver = 0
    return devolver
    
    
def hay_ayuda(linea):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de un archivo de comentarios.csv abierto y devuelve SI/NO indicando que hay descripcion de uso de la funcion.]
    """
    lista = linea.split(",")
    if lista[2] == " '[Ayuda: Sin ayuda]'":
        devolver = "NO"
    else:
        devolver = "SI"
    return devolver
    
def buscar_dueño(linea):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de comentarios.csv y devuelve el primer campo. Osea el autor.]
    """
    lista = linea.split(",")
    return lista[1]
    
    
def escribir_panel_general(arch_salida, funcion, parametros, lineas, invocaciones, returns, ifs, fors, whiles, breaks, exits, coments, ayudas, autores):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Escribe y genera un archivo de salida. Recibe en el primer parametro el archivo de salida y en el resto de los parametros, los valores de lo que hay que escribir.]
    """
    escribir = funcion + ", " + str(parametros) + ", " + str(lineas) + ", " + str(invocaciones)+ ", " + str(returns) + ", " + str(ifs) + ", " + str(fors) + ", " + str(whiles) + ", " + str(breaks) + ", " + str(exits) + ", " + str(coments) + ", " + ayudas + ", " + autores + "\n"
    arch_salida.write(escribir)
    
    
def count_invocaciones(fuente_unico):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una linea de un archivo de fuente_unico.csv abierto y devuelve un diccionario que tiene registrado la cantidad de invocaciones de cada funcion.]
    """
    l_funciones = []
    dic_contador = {}
    fuente_unico.seek(0)
    linea = fuente_unico.readline()
    # Recorro una primera vez para crearme una lista con todas las funciones.
    while linea:
        splits = linea.split(",")
        l_funciones.append(splits[0])
        linea = fuente_unico.readline()
    # Y luego vuelvo a recorrer el archivo por cada funcion que haya para contar cuantas invocaciones hay, guardandolas en un dic.
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
        # En caso de que haya un funcion que no tenga invocaciones (osea que no entro en la condicion anterior), la guardo aca.
        if l_funciones[i] not in dic_contador:
            dic_contador[l_funciones[i]] = 0
            
    return dic_contador

def main_panel_general_funciones(fuente_unico, comentarios, arch_salida):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe como entrada fuente_unico.csv, comentarios.csv y un archivo de salida ya abiertos. Imprime por pantalla todos los datos pedidos en el enunciado y los guarda en panel_general.csv.]
    """
    dic_invocaciones = count_invocaciones(fuente_unico)
    fuente_unico.seek(0)
    linea = fuente_unico.readline()
    linea_c = comentarios.readline()
    arch_salida.write("FUNCION, PARAMETROS, LINEAS, INVOCACIONES, RETURNS, IF, FOR, WHILE, BREAKS, EXITS, COMENTS, AYUDAS, AUTORES\n")
    print('{:^65}{:^10}{:^10}{:^10}{:^10}{:^10}{:^5}{:^10}{:^10}{:^10}{:^10}{:^10}{:^25}'.format("FUNCION", "Parámetros", "Líneas","Invocaciones","Returns","If/elif","for","while","break","Exit","Coment","Ayuda", "Autor"))
    
    while linea:
        # Ambos archivos tienen la misma cantidad de lineas asi que van a terminar al mismo tiempo.
        l_funcion_actual = linea.split(",")
        funcion_actual = l_funcion_actual[0]
        escribir_panel_general(arch_salida, buscar_funcion_modulo(linea), count_parametros(linea), count_lineas_codigo(linea), dic_invocaciones[funcion_actual], count_palabra(linea, "return"), count_ifs(linea), count_palabra(linea, "for"), count_palabra(linea, "while"), count_palabra(linea, "break"), count_palabra(linea, "exit"), count_comentarios(linea_c), hay_ayuda(linea_c), buscar_dueño(linea_c))
        print('{:^65}{:^10}{:^10}{:^10}{:^10}{:^10}{:^5}{:^10}{:^10}{:^10}{:^10}{:^10}{:^25}'.format(buscar_funcion_modulo(linea), count_parametros(linea), count_lineas_codigo(linea), dic_invocaciones[funcion_actual],count_palabra(linea, "return"),count_ifs(linea),count_palabra(linea, "for"),count_palabra(linea, "while"),count_palabra(linea, "break"),count_palabra(linea, "exit"),count_comentarios(linea_c),hay_ayuda(linea_c), buscar_dueño(linea_c))) 
        linea = fuente_unico.readline()
        linea_c = comentarios.readline()
             
    print("-------------------------------------------------------")
    print("\nGenere el panel general.csv")
    print("*Los datos han sido registrados en panel_general.csv, ubicado en la carpeta de salidas_modulos")
    