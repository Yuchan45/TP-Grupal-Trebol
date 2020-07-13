def capicuas(list_words):
    """
    [Autor: Yuchan]
    [Ayuda: Arma una lista con las palabras capicuas]
    """
    len_lista = len(list_words)
    for i in range(len_lista):
        palabra = list_words[i].lower()
        # asdas
        invertida = ""
        for j in range(len(palabra)-1, -1, -1):
            invertida += palabra[j]
        if palabra == invertida:
            # asdasdasdasads
            lista_capicuas.append(palabra)
    return lista_capicuas

def delete_repeated(lista):
    """
    [Autor: Yuchan]
    [Ayuda: Elimina elementos de la lista repetidos]
    """
    new_list = []
    long = len(lista)
    for i in range(long):
        # holas
        if not lista[i] in new_list:
            new_list.append(lista[i])
            #como
    return new_list


def make_list(txt):
    """
    [Ayuda: Arma una lista]
    """
    word_list = txt.split() # Side comment
    # Holaa
    return word_list
 




def ordered_list(lista):
    # Ordena alfabeticamente
    sorted_list = sorted(lista, key=str.lower)#asdasd
    return sorted_list


texto = str(input('Ingrese palabras separadas por espacios en blanco:'))
lista_palabras = make_list(texto)
lista_capicuas = capicuas(lista_palabras)
lista_sin_repetir = delete_repeated(lista_capicuas)
print(ordered_list(lista_sin_repetir))