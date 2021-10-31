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
    -Duración en segundos

    Retorna el analizador inicializado.
    """
    analyzer = {'avistamientos': None,
                'fecha': None,
                'duracion en seg': None
                }

    analyzer['avistamientos'] = lt.newList('SINGLE_LINKED', comparedates)
    analyzer['fecha'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareobjets)
    analyzer['duracion en seg']= om.newMap(omaptype='RBT',
                                      comparefunction=compareobjets)
    
    
    return analyzer

# Funciones para agregar informacion al catalogo

def addAvistamiento(analyzer, avistamiento):
    """
    """
    lt.addLast(analyzer['avistamientos'], avistamiento)
    updateDate(analyzer['fecha'], avistamiento)
    updateDuracionSeg(analyzer['duracion en seg'], avistamiento)
    return analyzer

def updateDuracionSeg(map, avistamiento):
    """
    Se toma la duración en segundos del avistamiento y se busca si ya existe en el arbol
    dicha duración.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa duración en el arbol
    se crea y se actualiza el indice de ciudades
    """
    duration = avistamiento['duration (seconds)']
    entry = om.get(map, duration)
    if entry is None:
        datentry = newDataEntry(avistamiento)
        om.put(map, duration, datentry)
    else:
        datentry = me.getValue(entry)
    return map

def updateDate(map, avistamiento):
    """
    Se toma la fecha del avistamiento y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de tipos de crimenes.

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

def addCityIndex(datentry, avistamiento):
    """
    Actualiza un indice de ciudad.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la ciudad de avistamiento y
    el valor es una lista con los avistamientos de dicha ciudad en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstavistamientos']
    lt.addLast(lst, avistamiento)
    DateIndex = datentry['Date']
    offentry = m.get(DateIndex, avistamiento['city'])
    if (offentry is None):
        entry = newCityEntry(avistamiento['city'], avistamiento)
        lt.addLast(entry['lstcities'], avistamiento)
        m.put(DateIndex, avistamiento['city'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], avistamiento)
    return datentry


def newDataEntry(avistamiento):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'Date': None, 'lstavistamientos': None}
    entry['Date'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=comparedates)
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED', comparedates)
    return entry

def newCityEntry(ciudad, avistamiento):
    """
    Crea una entrada en el indice por ciudad, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'city': None, 'lstcities': None}
    ofentry['city'] = ciudad
    ofentry['lstcities'] = lt.newList('SINGLELINKED', compareobjets)
    return ofentry

# Funciones para creacion de datos

# ==============================
# Funciones de consulta
# ==============================


def avistamientosSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['avistamientos'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['fecha'])


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

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# ==============================
# Funciones de Comparacion
# ==============================


def comparedates(date1, date2):
    """
    Compara dos crimenes
    """
    if (datetime.datetime.stripdate(date1,'%Y-%m-%d') == datetime.datetime.stripdate(date2,'%Y-%m-%d')):
        return 0
    elif (datetime.datetime.stripdate(date1,'%Y-%m-%d') > datetime.datetime.stripdate(date2,'%Y-%m-%d')):
        return 1
    else:
        return -1

def compareobjets(objet1, objet2):
    """
    Compara dos objetos
    """
    if (objet1 == objet2):
        return 0
    elif objet1 > objet2:
        return 1
    else:
        return -1
