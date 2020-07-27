def lista_de_funciones(fuente_unico):
    """[Autor: Carlos Medina]
       [Ayuda: Recibe una linea de fuente_unico.csv por parametro y devuelve una lista que contiene los nombres de las funciones]
    """
    lista_funciones = []
    
    linea_f = fuente_unico.readline()
    while linea_f:
        aux = linea_f.split(",")
        lista_funciones.append(aux[0])
        linea_f = fuente_unico.readline()

    return lista_funciones

def conseguir_funcion(palabra):
    """[Autor: Carlos Medina]
       [Ayuda: Recibe una palabra y devuelve la misma palabra separada por el caracter especial]
    """
    if "?" in palabra:
        aux = palabra.split("?")
        devolver = aux[0]
    elif "#" in palabra:
        aux = palabra.split("#")
        devolver = aux[0]
    else:
        devolver = palabra
    return devolver

def encontrar_funcion(linea):
    """[Autor: Carlos Medina]
       [Ayuda: recibe una linea de un archivo. La convierte a una lista separada por comas y devuelve el primer elemento que corresponde al nombre de la funcion]
    """
    lista = linea.split(",")
    return lista[0]

def encontrar_autor(linea):
    """[Autor: Carlos Medina]
       [Ayuda: recibe una linea de un archivo. La convierte a una lista separada por comas y devuelve el segundo elemento que corresponde al autor de la funcion]
    """
    lista = linea.split(",")
    return lista[1].lstrip("'[").rstrip("]'")

def encontrar_modulo(linea):
    """[Autor: Carlos Medina]
       [Ayuda: recibe una linea de un archivo. La convierte a una lista separada por comas y devuelve el modulo de la funcion]
    """
    lista = linea.split(",")
    for campo in lista:
        if ".py'" in campo:
            devolver = campo
    return devolver

def encontrar_param(linea):
    """[Autor: Carlos Medina]
       [Ayuda: recibe una linea de un archivo. La convierte a una lista separada por comas y devuelve el segundo elemento que corresponde a los parametros de la funcion]
    """
    lista = linea.split("'")
    devolver = lista[1]
    return devolver

def encontrar_descripcion(linea):
    """[Autor: Carlos Medina]
       [Ayuda: recibe una linea de un archivo. La convierte a una lista separada por comas y devuelve la ayuda de la funcion]
    """
    devolver = "Sin ayuda o descripcion."
    lista = linea.split("]', ")
    for campo in lista:
        if "ayuda:" in campo.lower():
            devolver = campo.lstrip("'[").rstrip("]'")
    return devolver

def enc_extra_descripcion(linea):
    """[Autor: Carlos Medina]
       [Ayuda: recibe una linea de un archivo. La convierte a una lista separada por comas y devuelve el resto de la ayuda, si dentro de la misma existe una coma]
    """
    devolver = []
    lista = linea.split("]',")
    # Las ayudas y autores estan definidos entre " [ ] ".
    if len(lista) > 2:
        comentarios_extra = lista[2].split("',")
        devolver = comentarios_extra
    else:
        devolver = ["Sin comentarios extra descripcion."]
        
    return devolver

def lista_lineas_de_codigo(linea):
    """[Autor: Carlos Medina]
       [Ayuda: Recibe una linea de fuente_unico y abierta. Y devuelve una lista con las lineas de CODIGO (Sin espacios en blanco)]
    """
    lista_sin_vacios = []  
    linea = linea.rstrip("\n")
    lista = linea.split(".py', ") # La lista[1] va a tener todo lo que le sigue al modulo, osea el codigo.
    lista_linea_codigo = lista[1].split("', ") # lista_linea_codigo va a ser una lista con todo lo que le sigue al campo de modulo. Osea codigo puro
    # Elimino los espacios en blanco. Creo una lista vacia y meto los campos no vacios.
    for campo in lista_linea_codigo:
        if campo != "''" and campo != "'":
            lista_sin_vacios.append(campo)
    #print(lista_sin_vacios)
    return lista_sin_vacios


def caso_pregunta(fuente_unico, comentarios, funcion):
    """[Autor: Carlos Medina]
       [Ayuda: recibe los archivos, fuente_unico y comentarios y la funcion elegida por el usuario, luego imprime el autor, la ayuda, los parametros y el modulo de la funcion buscada]
    """
    fuente_unico.seek(0)
    comentarios.seek(0)
    linea_f = fuente_unico.readline()
    linea_c = comentarios.readline()
    while linea_f and linea_c:   
        funcion_linea = encontrar_funcion(linea_c) 
        if funcion_linea == funcion:
            print("\n-----------------------------------------------")
            print("|Funcion|: ", funcion + encontrar_param(linea_f))
            print("|INFORMACION|:\n---------------")
            print(encontrar_autor(linea_c))
            print(encontrar_descripcion(linea_c))
            print("Funcion utilizada en el modulo: " + encontrar_modulo(linea_f))
            print("-----------------------------------------------\n\n")     
        linea_f = fuente_unico.readline()
        linea_c = comentarios.readline()


def caso_hashtag(fuente_unico, comentarios, funcion):
    """[Autor: Carlos Medina]
       [Ayuda: Recibe fuente_unico, comentarios y la funcion buscada por parametro. Imprime los datos solicitados por el enunciado.]
    """
    
    fuente_unico.seek(0)
    comentarios.seek(0)
    linea_f = fuente_unico.readline()
    linea_c = comentarios.readline()
    while linea_f and linea_c:   
        funcion_linea = encontrar_funcion(linea_c) 
        if funcion_linea == funcion:
            lista_extra_descripcion = enc_extra_descripcion(linea_c)
            print("\n-----------------------------------------------")
            print("|Funcion|: ", funcion + encontrar_param(linea_f))
            print("|INFORMACION|:\n---------------")
            print(encontrar_autor(linea_c))
            print(encontrar_descripcion(linea_c))
            print("Funcion utilizada en el modulo: " + encontrar_modulo(linea_f) + "\n")
            print("|COMENTARIOS EXTRA DESCRIPCION|:")
            for i in range(len(lista_extra_descripcion)):
                print(lista_extra_descripcion[i].rstrip("'").lstrip("'"))
            print("-----------------CODIGO--------------------")
            lista_codigo = lista_lineas_de_codigo(linea_f)
            for campo in range(len(lista_codigo)):
                print(lista_codigo[campo].lstrip("'") + "\n")
            print("-----------------------------------------------\n\n")     
        linea_f = fuente_unico.readline()
        linea_c = comentarios.readline()


def caso_pregunta_todo(fuente_unico, comentarios):
    """[Autor: Carlos Medina]
       [Ayuda: recibe los archivos, fuente_unico y comentarios. Luego imprime el autor, la ayuda, los parametros y el modulo para cada una de las funciones mostradas por pantalla]
    """
    # Muestra autor, ayuda, parametros y modulo de la funcion buscada.
    fuente_unico.seek(0)
    comentarios.seek(0)
    linea_f = fuente_unico.readline()
    linea_c = comentarios.readline()
    while linea_f and linea_c:
        print("\n-----------------------------------------------")
        print("|Funcion|: " + encontrar_funcion(linea_c) + encontrar_param(linea_f))
        print("|INFORMACION|:\n---------------")
        print(encontrar_autor(linea_c))
        print(encontrar_descripcion(linea_c))
        print("Funcion utilizada en el modulo: " + encontrar_modulo(linea_f))
        print("-----------------------------------------------\n\n")     
        linea_f = fuente_unico.readline()
        linea_c = comentarios.readline()
        
        
def caso_hashtag_todo(fuente_unico, comentarios):
    """[Autor: Carlos Medina]
       [Ayuda: recibe los archivos, fuente_unico y comentarios. Luego imprime todo lo relativo a la funcion, para cada una de las funciones mostradas por pantalla]
    """
    fuente_unico.seek(0)
    comentarios.seek(0)
    linea_f = fuente_unico.readline()
    linea_c = comentarios.readline()
    while linea_f and linea_c:
        lista_extra_descripcion = enc_extra_descripcion(linea_c)
        lista_codigo = lista_lineas_de_codigo(linea_f)
        print("\n-----------------------------------------------")
        print("|Funcion|: ", encontrar_funcion(linea_c) + encontrar_param(linea_f))
        print("|INFORMACION|:\n---------------")
        print(encontrar_autor(linea_c))
        print(encontrar_descripcion(linea_c))
        print("Funcion utilizada en el modulo: " + encontrar_modulo(linea_f) + "\n")
        print("|COMENTARIOS EXTRA DESCRIPCION|:")
        for i in range(len(lista_extra_descripcion)):
            print(lista_extra_descripcion[i].lstrip("'").rstrip("'"))
        print("-----------------CODIGO--------------------")
        for campo in range(len(lista_codigo)):
            print(lista_codigo[campo].lstrip("'").rstrip("\n") + "\n")
        print("-----------------------------------------------\n\n")     
        linea_f = fuente_unico.readline()
        linea_c = comentarios.readline()
        
        
def caso_imprimir_todo(fuente_unico, comentarios, arch_salida):
    """[Autor: Carlos Medina]
       [Ayuda: Recibe fuente_unico, comentarios y un archivo de salida previamente abiertos. Escribe en el archivo de salida los datos solicitados por el enunciado haciendo uso de la funcion "escribir-salida"]
    """
    fuente_unico.seek(0)
    comentarios.seek(0)
    linea_f = fuente_unico.readline()
    linea_c = comentarios.readline()
    while linea_f and linea_c:
        funcion = encontrar_funcion(linea_c)
        autor = encontrar_autor(linea_c)
        descripcion = encontrar_descripcion(linea_c)
        parametros = encontrar_param(linea_f)
        modulo = encontrar_modulo(linea_f)
        
        escribir_arch_salida(arch_salida, funcion, parametros, autor, descripcion, modulo)
        
        linea_f = fuente_unico.readline()
        linea_c = comentarios.readline()
    print("* Genere el archivo 'ayuda_funciones.txt'. Se encuentra en la carpeta 'salidas_modulos'")

def mostrar_cuadro(lista_funciones):
    """[Autor: Carlos Medina]
       [Ayuda: A esta funcion le llega por parametro una lista con los nombres de todas las funciones
       e imprime estos nombres con un formato (5 columnas, x filas)]
    """
    i = 0
    print("----------------------TABLA DE FUNCIONES--------------------------")
    while len(lista_funciones) % 5 != 0:
        lista_funciones.append(" ") 
    while i < len(lista_funciones):
        print("|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|\n".format(lista_funciones[i], lista_funciones[i+1], lista_funciones[i+2], lista_funciones[i+3], lista_funciones[i+4]))
        i += 5
    print("\n")
        
def escribir_arch_salida(salida, funcion, parametros, autor, descripcion, modulo):
    """[Autor: Carlos Medina]
       [Ayuda: Recibe por parametros los datos a escribir en el archivo de salida. Devuelve un txt ubicado en salidas_modulos con todos los datos.]
    """
    max = 80
    salida.write("-----------------------------------------------\n")
    escribir = "|Funcion|: " + str(funcion) + str(parametros) + "\n"
    # Se fija de que el string a escribir no supere los 80 caracteres. Si los supera, hace un enter y vuelve a escribir la continuacion en el renglon de abajo.
    if len(escribir) > max:
        for i in range(0, len(escribir), max):
            salida.write(escribir[i: i + max] + "\n")
    else:
        salida.write(escribir + "\n")
    salida.write("|INFORMACION|:\n---------------\n")
    salida.write(autor + "\n")
    
    if len(descripcion) > max:
        for i in range(0, len(descripcion), max):
            salida.write(descripcion[i: i + max] + "\n")
    else:
        salida.write(descripcion + "\n")
        
    escribir = "Funcion utilizada en el modulo: " + str(modulo) + "\n"
    if len(escribir) > max:
        for i in range(0, len(escribir), max):
            salida.write(escribir[i: i + max] + "\n")
    else:
        salida.write(escribir + "\n")
    salida.write("-----------------------------------------------\n\n")
      

def main_consulta_funciones(fuente_unico, comentarios, arch_salida, lista_funciones):
    """[Autor: Carlos Medina]
       [Ayuda: Recibe por parametros fuente_unico, camentarios, el archivo de salida, todos previamente abiertos y una lista con las funciones que hay. Pregunta que es lo que es usuario desea realizar y dependiendo de lo que eliga, ejecuta la funcion correspondiente.]
    """
    print("'funcion + ?' para ver autor, ayuda, parametros y modulo.")
    print("'funcion + #' para ver todo lo relativo a la funcion.")
    print("'?todo' para ver el autor, ayuda, parametros y modulos de TODAS las funciones.")
    print("'#todo' para ver todo lo relativo a TODAS las funciones.")
    print("'imprimir ?todo' para guardar todos los datos en ayuda_funciones.txt \n")
    
    print("(Para terminar toque enter sin ingresar nada.)")
    entrada = str(input("Funcion: ")) 
    while entrada != "":
        funcion = conseguir_funcion(entrada)
        
        if funcion in lista_funciones and entrada.endswith("?"):
            caso_pregunta(fuente_unico, comentarios, funcion)
        elif funcion in lista_funciones and entrada.endswith("#"):
            caso_hashtag(fuente_unico, comentarios, funcion)
        elif entrada == "?todo":
            caso_pregunta_todo(fuente_unico, comentarios)
        elif entrada == "#todo":
            caso_hashtag_todo(fuente_unico, comentarios)
        elif entrada == "imprimir ?todo":
            caso_imprimir_todo(fuente_unico, comentarios, arch_salida)
        else:
            print("'funcion + ?' para ver autor, ayuda, parametros y modulo.")
            print("'funcion + #' para ver todo lo relativo a la funcion.")
            print("'funcion + ?todo' para ver el autor, ayuda, parametros y modulos de TODAS las funciones.")
            print("'funcion + #todo' para ver todo lo relativo a TODAS las funciones.")
            print("'imprimir ?todo' para guardar todos los datos en ayuda_funciones.txt")
            
        print("(Para terminar toque enter sin ingresar nada.)")
        entrada = str(input("Funcion: ")) 

