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



from DISClib.DataStructures.arraylist import compareElements
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import quicksort as sa
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
                'ciudad': None,
                'duracion': None,
                'time': None,
                'longitud': None
                }

    analyzer['avistamientos'] = lt.newList('SINGLE_LINKED', compareElements)
    analyzer['fecha'] = om.newMap(omaptype='BST')
    analyzer['ciudad'] = om.newMap(omaptype='BST') 
    analyzer['duracion'] = om.newMap(omaptype='BST') 
    analyzer['time'] = om.newMap(omaptype='BST') 
    analyzer['longitud'] = om.newMap(omaptype='BST')                                   
    return analyzer

# Funciones para agregar informacion al catalogo

def addAvistamiento(analyzer, avistamiento):
    """
    """
    lt.addLast(analyzer['avistamientos'], avistamiento)
    updateDate(analyzer['fecha'], avistamiento)
    updateCity(analyzer['ciudad'], avistamiento)
    updateDuracion(analyzer['duracion'], avistamiento)
    updateTime(analyzer['time'], avistamiento)
    updateLongitud(analyzer['longitud'], avistamiento)
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

def updateTime(map, avistamiento):
    """
    Se toma la hora del avistamiento y se busca si ya existe en el arbol
    dicha hora.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de ciudad.

    Si no se encuentra creado un nodo para esa duración en el arbol
    se crea y se actualiza el indice de ciudad de avistamiento
    """
    occurredtime = avistamiento['datetime']
    hora = occurredtime[11:19] 
    time = datetime.datetime.strptime(hora, '%H:%M:%S')
    entry = om.get(map, time.date())
    if entry is None:
        Timeentry = newtimeEntry(avistamiento)
        om.put(map, time.date(), Timeentry)
    else:
        Timeentry = me.getValue(entry)
    addcityIndex(Timeentry, avistamiento)
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

def updateDuracion(map, avistamiento):
    """
    Se toma la duración del avistamiento y se busca si ya existe en el arbol
    dicha duración.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de ciudad.

    Si no se encuentra creado un nodo para esa duración en el arbol
    se crea y se actualiza el indice de ciudad de avistamiento
    """
    occurredcity = avistamiento['duration (seconds)']
    entry = om.get(map, occurredcity)
    if entry is None:
        durationentry = newDurationEntry(avistamiento)
        om.put(map, occurredcity, durationentry)
    else:
        durationentry = me.getValue(entry)
    addCountryIndex(durationentry, avistamiento)
    return map

def updateLongitud(map, avistamiento):
    """
    Se toma la longitud del avistamiento y se busca si ya existe en el arbol
    dicha longitud.  Si es asi, se adiciona a su lista de avistamientos
    y se actualiza el indice de latitud.

    Si no se encuentra creado un nodo para esa longitud en el arbol
    se crea y se actualiza el indice de latitud de avistamiento
    """
    longitud = avistamiento['longitude']
    entry = om.get(map, longitud)
    if entry is None:
        longitudentry = newLongitudEntry(avistamiento)
        om.put(map, longitud, longitudentry)
    else:
        longitudentry = me.getValue(entry)
    addLongitudIndex(longitudentry, avistamiento)
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

def addcityIndex(datentry, avistamiento):
    """
    Actualiza un indice de hora.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la hora del avistamiento y
    el valor es una lista con los avistamientos de dicha hora en la ciudad que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstavistamientos']
    lt.addLast(lst, avistamiento)
    DateIndex = datentry['city']
    offentry = m.get(DateIndex, avistamiento['city'])
    if (offentry is None):
        entry = newHourEntry(avistamiento['city'], avistamiento)
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

def addCountryIndex(datentry, avistamiento):
    """
    Actualiza un indice de duración.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la duración del avistamiento y
    el valor es una lista con los avistamientos de dicha ciudad en el país que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstavistamientos']
    lt.addLast(lst, avistamiento)
    DateIndex = datentry['duration']
    offentry = m.get(DateIndex, avistamiento['duration (seconds)'])
    if (offentry is None):
        entry = newCountryEntry(avistamiento['duration (seconds)'], avistamiento)
        lt.addLast(entry['lstcountries'], avistamiento)
        m.put(DateIndex, avistamiento['duration (seconds)'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstcountries'], avistamiento)
    return datentry

def addLongitudIndex(datentry, avistamiento):
    """
    Actualiza un indice de longitud.  Este indice tiene una lista
    de avistamientos y una tabla de hash cuya llave es la longitud del avistamiento y
    el valor es una lista con los avistamientos de dicha longitud en la latitud que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstavistamientos']
    lt.addLast(lst, avistamiento)
    DateIndex = datentry['longitud']
    offentry = m.get(DateIndex, avistamiento['longitude'])
    if (offentry is None):
        entry = newLatitudEntry(avistamiento['longitude'], avistamiento)
        lt.addLast(entry['lstlatitudes'], avistamiento)
        m.put(DateIndex, avistamiento['longitude'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstlatitudes'], avistamiento)
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

#/////////////////////NewEntry/////////////////////

def newDataEntry(avistamiento):
    """
    Crea una entrada en el indice por ciudades, es decir en el arbol
    binario.
    """
    entry = {'city': None, 'lstavistamientos': None}
    entry['city'] = m.newMap(numelements=30,
                                     maptype='PROBING')
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED')
    return entry

def newtimeEntry(avistamiento):
    """
    Crea una entrada en el indice por hora, es decir en el arbol
    binario.
    """
    entry = {'city': None, 'lstavistamientos': None}
    entry['city'] = m.newMap(numelements=30,
                                     maptype='PROBING')
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED')
    return entry

def newCityEntry(avistamiento):
    """
    Crea una entrada en el indice por duraciones, es decir en el arbol
    binario.
    """
    entry = {'time': None, 'lstavistamientos': None}
    entry['time'] = m.newMap(numelements=30,
                                     maptype='PROBING')
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED')
    return entry

def newFechaEntry(ciudad, avistamiento):
    """
    Crea una entrada en el indice por ciudad, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'city': None, 'lstcities': None}
    ofentry['city'] = ciudad
    ofentry['lstcities'] = lt.newList('SINGLELINKED')
    return ofentry

def newHourEntry(ciudad, avistamiento):
    """
    Crea una entrada en el indice por ciudad, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'city': None, 'lstcities': None}
    ofentry['city'] = ciudad
    ofentry['lstcities'] = lt.newList('SINGLELINKED')
    return ofentry

def newDurationEntry(avistamiento):
    """
    Crea una entrada en el indice por duraciones, es decir en el arbol
    binario.
    """
    entry = {'duration': None, 'lstavistamientos': None}
    entry['duration'] = m.newMap(numelements=30,
                                     maptype='PROBING')
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED')
    return entry


def newLongitudEntry(avistamiento):
    """
    Crea una entrada en el indice por longitudes, es decir en el arbol
    binario.
    """
    entry = {'longitd': None, 'lstavistamientos': None}
    entry['longitud'] = m.newMap(numelements=30,
                                     maptype='PROBING')
    entry['lstavistamientos'] = lt.newList('SINGLE_LINKED')
    return entry


def newTimeEntry(ciudad, avistamiento):
    """
    Crea una entrada en el indice por tiempo, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'time': None, 'lsttimes': None}
    ofentry['time'] = ciudad
    ofentry['lsttimes'] = lt.newList('SINGLELINKED')
    return ofentry

def newCountryEntry(ciudad, avistamiento):
    """
    Crea una entrada en el indice por país, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'country': None, 'lstcountries': None}
    ofentry['country'] = ciudad
    ofentry['lstcountries'] = lt.newList('SINGLELINKED')
    return ofentry

def newLatitudEntry(ciudad, avistamiento):
    """
    Crea una entrada en el indice por país, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'latitud': None, 'lstlatitudes': None}
    ofentry['latitud'] = ciudad
    ofentry['lstlatitudes'] = lt.newList('SINGLELINKED')
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

def citySize(analyzer):
    """
    Altura del arbol de ciudades
    """
    return om.size(analyzer['ciudad'])


def durationSize(analyzer):
    """
    Altura del arbol de duraciones
    """
    return om.size(analyzer['duracion'])

def TimeSize(analyzer):
    """
    Altura del arbol de horas
    """
    return om.size(analyzer['time'])

def LongitudSize(analyzer):
    """
    Altura del arbol de longitudes
    """
    return om.size(analyzer['longitud'])


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
    totavistamientos = 0
    for lstdate in lt.iterator(lst):
        totavistamientos += lt.size(lstdate['lstavistamientos'])
                
    return totavistamientos

def getAvistamientosByCity(analyzer, city):

    keys = om.keySet(analyzer['ciudad'])
    values = om.valueSet(analyzer['ciudad'])
    pos = lt.isPresent(keys, city)
    lst = lt.getElement(values, pos)
    size = lt.size(lst['lstavistamientos'])
    
    print("\nTotal de avistamientos en la ciudad dada: " + str(size))

    if size <= 6:
        return lst
    else: 
        lst1 = lt.subList(lst['lstavistamientos'], 1, 3)
        lst2 = lt.subList(lst['lstavistamientos'], size-3, 3)
        

        for x in lt.iterator(lst1):
            print("datetime: " + str(x['datetime']) + " city: " + str(x['city']) + " state: " + str(x['state']) + " country: " + str(x['country']) +  " shape: " + str(x['shape']))

        for x in lt.iterator(lst2):
            print("datetime: " + str(x['datetime']) + " city: " + str(x['city']) + " state: " + str(x['state']) + " country: " + str(x['country']) +  " shape: " + str(x['shape']))
        
        
        for x in lt.iterator(lst1):
            print("datetime: " + str(x['datetime']) + " city: " + str(x['city']) + " state: " + str(x['state']) + " country: " + str(x['country']) +  " shape: " + str(x['shape']))

        for x in lt.iterator(lst2):
            print("datetime: " + str(x['datetime']) + " city: " + str(x['city']) + " state: " + str(x['state']) + " country: " + str(x['country']) +  " shape: " + str(x['shape']))
        
             


def get5bestcities(analyzer):
    """
    Retorna las 5 ciudades con más avistamientos
    """

    keys = om.keySet(analyzer['ciudad'])
    values = om.valueSet(analyzer['ciudad'])
    cantidad = lt.newList()

    for value in lt.iterator(values):
        if value is not None:
            size = lt.size(value['lstavistamientos'])
            lt.addLast(cantidad, size)
    
    i = 0
    while i <= 4:
        pos = getbest(cantidad)
        city = lt.getElement(keys, pos)
        cant = lt.getElement(cantidad, pos)
        print ("Ciudad: " + str(city) + "; Cantidad: " + str(cant))
        lt.deleteElement(keys, pos)
        lt.deleteElement(cantidad, pos)
        i += 1

def get5bestdurations(analyzer):
    """
    Retorna las 5 duraciones más largas
    """
    keys = om.keySet(analyzer['duracion'])
    values = om.valueSet(analyzer['duracion'])
  
    i = 0
    while i < 5:

        mejor = 0
        value = 0
    
        for key in lt.iterator(keys):
            if key is not None:
                if float(key) < lt.size(keys): 
                    if float(lt.getElement(keys, float(key))) > mejor:
                        mejor = float(lt.getElement(keys, float(key)))
                        pos = lt.isPresent(keys, lt.getElement(keys, float(key)))
                        value = lt.getElement(values, pos)
        
        print ("Duración (Segundos): " + str(mejor) + "; Cantidad: " + str(lt.size(value['lstavistamientos'])))
        lt.deleteElement(keys, pos)
        lt.deleteElement(values, pos)
        
        i += 1

 
def getbest(lista):

    mejor = 0
    pos = 0
    for elm in lt.iterator(lista):
        x = lt.getElement(lista, elm)
        
        y = lt.isPresent(lista, elm)
        if x > mejor:
            mejor = x
            pos = y
    
    return (pos)
    

def getAvistamientosByDuration(analyzer, min, max):

    values = om.values(analyzer['duracion'], max, min)
    size = lt.size(values)
    
    totavistamientos = 0
    for lstduration in lt.iterator(values):
        totavistamientos += lt.size(lstduration['lstavistamientos'])
    
                
    return totavistamientos

def getavistamientos(analyzer, longitud1, longitud2, latitud1, latitud2):

    longitudes = om.values(analyzer['longitud'], longitud1, longitud2)
    size = lt.size(longitudes)
    finales = lt.newList()
       
    for i in range(1, int(size), 1):
        value = lt.getElement(longitudes, i)
        x = lt.size(value['lstavistamientos'])
        for b in range(1, int(x), x):
            value2 = lt.getElement(value['lstavistamientos'], b)
            if latitud1 <= value2['latitude'] <= latitud2:
                lt.addLast(finales, value2)
    
    cant =lt.size(finales)
    print("Cantidad de avistamientos en el rango: " + str(cant))

    if cant <= 6:
        for x in lt.iterator(finales):
            print("datetime: " + str(x['datetime']) + " city: " + str(x['city']) + " state: " + str(x['state']) + " country: " + str(x['country']) +  " shape: " + str(x['shape']))

    else: 
        i = 0
        while i < 3:
            x = lt.getElement(finales, i)
            y = lt.getElement(finales, size-i)

            
            print("datetime: " + str(x['datetime']) + " city: " + str(x['city']) + " state: " + str(x['state']) + " country: " + str(x['country']) +  " shape: " + str(x['shape']))
            print("datetime: " + str(y['datetime']) + " city: " + str(y['city']) + " state: " + str(y['state']) + " country: " + str(y['country']) +  " shape: " + str(y['shape']))

        


# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# ==============================
# Funciones de Comparacion
# ==============================

def comparedurations(duration1, duration2):
    return (duration1 > duration2)







