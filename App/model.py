"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """



import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'avistamientos': None,
                'fecha': None,
                'ciudad': None
                }

    analyzer['avistamientos'] = lt.newList('SINGLE_LINKED', comparedates)
    analyzer['fecha'] = om.newMap(omaptype='BST',
                                      comparefunction=comparedates)
    analyzer['ciudad'] = om.newMap(omaptype='BST',
                                      comparefunction=comparecities)                                  
    return analyzer

# Funciones para agregar informacion al catalogo

def addAvistamiento(analyzer, avistamiento):
    """
    """
    lt.addLast(analyzer['avistamientos'], avistamiento)
    updateDate(analyzer['fecha'], avistamiento)
    updateCity(analyzer['ciudad'], avistamiento)
    return analyzer

def updateDate(map, avistamiento):
    """
    Se toma la fecha del avistamiento y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de ciudades.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de ciudades
    """
    occurreddate = avistamiento['datetime']
    fecha = occurreddate[0:10]
    date = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    entry = om.get(map, date.date())
    if entry is None:
        datentry = newDataEntry(avistamiento)
        om.put(map, date.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addCityIndex(datentry, avistamiento)
    return map

def updateCity(map, avistamiento):
    """
    Se toma la ciudad del avistamiento y se busca si ya existe en el arbol
    dicha ciudad.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de tiempo de avistamiento.

    Si no se encuentra creado un nodo para esa ciudad en el arbol
    se crea y se actualiza el indice de tiempo de avistamiento
    """
    occurredcity = avistamiento['city']
    entry = om.get(map, occurredcity)
    if entry is None:
        cityentry = newCityEntry(avistamiento)
        om.put(map, occurredcity, cityentry)
    else:
        cityentry = me.getValue(entry)
    addTimeIndex(cityentry, avistamiento)
    return map

def addCityIndex(datentry, avistamiento):
    """
    Actualiza un indice de ciudad.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la ciudad de avistamiento y
    el valor es una lista con los avistamientos de dicha ciudad en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstavistamientos']
    lt.addLast(lst, avistamiento)
    DateIndex = datentry['city']
    offentry = m.get(DateIndex, avistamiento['city'])
    if (offentry is None):
        entry = newFechaEntry(avistamiento['city'], avistamiento)
        lt.addLast(entry['lstcities'], avistamiento)
        m.put(DateIndex, avistamiento['city'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstcities'], avistamiento)
    return datentry

def addTimeIndex(datentry, avistamiento):
    """
    Actualiza un indice de tiempo de avistamiento.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es el tiempo de avistamiento y
    el valor es una lista con los avistamientos de dicho tiempo en la ciudad que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstavistamientos']
    lt.addLast(lst, avistamiento)
    CityIndex = datentry['time']
    offentry = m.get(CityIndex, avistamiento['city'])
    if (offentry is None):
        entry = newTimeEntry(avistamiento['city'], avistamiento)
        lt.addLast(entry['lsttimes'], avistamiento)
        m.put(CityIndex, avistamiento['city'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lsttimes'], avistamiento)
    return datentry


def newDataEntry(avistamiento):
    """
    Crea una entrada en el indice por ciudades, es decir en el arbol
    binario.
    """
    entry = {'city': None, 'lstavistamientos': None}
    entry['city'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=comparecities)
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED', comparedates)
    return entry

def newCityEntry(avistamiento):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'time': None, 'lstavistamientos': None}
    entry['time'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=comparedates)
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED', comparedates)
    return entry

def newFechaEntry(ciudad, avistamiento):
    """
    Crea una entrada en el indice por ciudad, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'city': None, 'lstcities': None}
    ofentry['city'] = ciudad
    ofentry['lstcities'] = lt.newList('SINGLELINKED', comparecities)
    return ofentry

def newTimeEntry(ciudad, avistamiento):
    """
    Crea una entrada en el indice por tiempo, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'time': None, 'lsttimes': None}
    ofentry['time'] = ciudad
    ofentry['lsttimes'] = lt.newList('SINGLELINKED', comparecities)
    return ofentry



# Funciones para creacion de datos

# ==============================
# Funciones de consulta
# ==============================


def avistamientosSize(analyzer):
    """
    Número de avistamientos
    """
    return lt.size(analyzer['avistamientos'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['fecha'])

def cityHeight(analyzer):
    """
    Altura del arbol de ciudades
    """
    return om.height(analyzer['ciudad'])



def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['fecha'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['fecha'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['fecha'])

def getAvistamientosByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de avistamientos en un rago de fechas.
    """
    lst = om.values(analyzer['fecha'], initialDate, finalDate)
    totcrimes = 0
    for lstdate in lt.iterator(lst):
        totcrimes += lt.size(lstdate['lstavistamientos'])
                
    return totcrimes

def getAvistamientosByCity(analyzer, city):

    keys = om.keySet(analyzer['ciudad'])
    values = om.valueSet(analyzer['ciudad'])
    pos = lt.isPresent(keys, city) 
    lst = lt.getElement(values, pos)
    size = lt.size(lst)

    if size <= 6:
        return lst
    else: 
        lst1 = lt.subList(lst, 1, 3)
        lst2 = lt.subList(lst, size-3, 3)

        for x in lst2:
            elm = lt.getElement(lst2, x)
            lt.addLast(lst1,elm)
        return(lst1)


    



    


def get5bestcities(analyzer):
    """
    Retorna las 5 ciudades con más avistamientos
    """
    

    keys = om.keySet(analyzer['ciudad'])
    values = om.valueSet(analyzer['ciudad'])
    cantidad = lt.newList()

    for value in values:
        size = lt.size(value)
        lt.addLast(cantidad, size)

    i = 0
    while i <= 5:
        pos = getbest(cantidad)
        city = lt.getElement(keys, pos)
        cant = lt.getElement(cantidad, pos)
        print ("Ciudad: " + str(city) + "Cantidad: " + str(cant))
        lt.deleteElement(keys, pos)
        lt.deleteElement(cantidad, pos)
        i += 1
        
def getbest(lista):

    mejor = 0
    pos = 0

    for elm in lista:
        x = lt.getElement(lista, elm)
        if x > mejor:
            mejor = x
            pos = lt.isPresent(lista, x)
    return (pos)



        











# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# ==============================
# Funciones de Comparacion
# ==============================


def comparedates(date1, date2):
    """
    Compara dos crimenes
    """
    if (datetime.datetime.striptime(date1,'%Y-%m-%d') == datetime.datetime.striptime(date2,'%Y-%m-%d')):
        return 0
    elif (datetime.datetime.striptime(date1,'%Y-%m-%d') > datetime.datetime.striptime(date2,'%Y-%m-%d')):
        return 1
    else:
        return -1

def comparecities(city1, city2):
    """
    Compara dos crimenes
    """
    if (city1 == city2):
        return 0
    elif city1 > city2:
        return 1
    else:
        return -1
