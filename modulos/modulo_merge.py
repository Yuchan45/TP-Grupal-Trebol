MAX_NOM_FUNCION = "zzzzzzzzzzzzzzz"

def leer(arch):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe un archivo y lee una linea de este]
    """
    linea = arch.readline()
    if linea:
        devolver = linea.rstrip("\n").split(",")       
    else:
        devolver = (MAX_NOM_FUNCION, "fin")
    return devolver

def guardar(arch, nom_funcion, extras):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe un archivo abierto en el cual va a escribir (archivo de salida), y escribe en este el nombre de la funcion y el resto de los campos]
    """
    datos_extras = []
    # Transformo la lista en un string para poder escribirla.
    for extra in extras:
        datos_extras.append(str(extra))
    extras_formato = ",".join(datos_extras)
    arch.write(str(nom_funcion) + "," + extras_formato + "\n")
    
def leer_lineas(l_arch):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una lista de archivos y retorna la primer linea que leyo de cada archivo]
    """
    lineas = []
    for arch in l_arch:
        linea = leer(arch)
        lineas.append(linea)
    return lineas

def menor_funcion(lineas):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una lista con lineas y genera una lista ordenada alfabeticamente. Retorna el menor de la lista.]
    """
    dato_menor = min(lineas)
    return dato_menor[0]

def merge(arch_salida, *archs_entrada):
    """[Autor: Miguel Lora]
       [Ayuda: Recibe un archivo de salida "arch_salida" abierto en modo sobreescritura en donde se guardara el merge y "archs_entrada" la cual es una lista de archivos csv ya abiertos en modo lectura.]
    """
    lineas = leer_lineas(archs_entrada)
    menor = menor_funcion(lineas)
    
    while menor < MAX_NOM_FUNCION:
        for i in range(len(lineas)):
            # En nom_funcion guarda el primer campo y en "*extras" (variable dinamica) se guarda el resto de los campos.
            nom_funcion, *extras = lineas[i]
            #Guarda los datos de la línea mientras el nom_funcion no cambie
            while nom_funcion == menor:
                guardar(arch_salida, nom_funcion, extras)
                nom_funcion, *extras = leer(archs_entrada[i])
            #La línea que no cumplió la condición se guarda en la lista para el próximo ciclo
            lineas[i] = [nom_funcion, *extras]
            
        menor = menor_funcion(lineas)


def abrir_archivos(lista):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una lista y abre los archivos dentro de esta. Devuelve las rutas de los archivos en una lista]
    """
    rutas_arch_abiertos = []
    for i in range(len(lista)):
        rutas_arch_abiertos.append(open(lista[i], "r"))
    return rutas_arch_abiertos
   
def cerrar_archivos(lista):
    """[Autor: Tomas Yu Nakasone]
       [Ayuda: Recibe una lista con las rutas de los archivos a cerrar y los cierra]
    """
    for i in range(len(lista)):
        lista[i].close()

def main_modulo_merge(lista_funciones, lista_comentarios):
    """[Autor: Carlos Medina]
       [Ayuda: Recibe una lista con las rutas de los archivos a mergear (lsita_comentarios --> paths de los archivos de comentarios y lista_funciones --> paths de archivos de funciones). Genera "fuente_unico.csv" y "comentarios.csv"]
    """
    # Hago lo mismo 2 veces
    # ------------- comentarios.csv
    rutas_arch_abiertos = abrir_archivos(lista_comentarios) # Abro los archivos de la lista comentarios y obtegno una lista con los paths de los archivos a mergear
    salida = "comentarios.csv"
    arch_salida = open(salida, "w")
    
    merge(arch_salida, *rutas_arch_abiertos) # Le pase una lista como variable dinamica. Le pasa todos lo archivos abiertos que tengo guardado en la lista rutas
    
    arch_salida.close()
    cerrar_archivos(rutas_arch_abiertos) # Cierro los csv que use para mergear
    
    # ------------- fuente_unico.csv
    rutas_arch_abiertos = abrir_archivos(lista_funciones) 
    salida = "fuente_unico.csv"
    arch_salida = open(salida, "w")
    
    merge(arch_salida, *rutas_arch_abiertos)

    
    arch_salida.close()
    cerrar_archivos(rutas_arch_abiertos) 
    
    
    
    
    
    
