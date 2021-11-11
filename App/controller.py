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
 """

import config as cf
import model
import csv
import datetime
from DISClib.ADT import list as lt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, UFOSfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    UFOSfile = cf.data_dir + UFOSfile
    input_file = csv.DictReader(open(UFOSfile, encoding="utf-8"),
                                delimiter=",")
    for avistamiento in input_file:
        model.addAvistamiento(analyzer, avistamiento)
    return analyzer

# Funciones de ordenamiento

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def avistamientosSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.avistamientosSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)

def citySize(analyzer):
    """
    Altura del arbol de ciudades
    """
    return model.citySize(analyzer)

def durationSize(analyzer):
    """
    Altura del arbol de duraciones
    """
    return model.durationSize(analyzer)

def TimeSize(analyzer):
    """
    Altura del arbol de horas
    """
    return model.TimeSize(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

def getAvistamientosByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de avistamientos en un rango de fechas
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAvistamientosByRange(analyzer, initialDate.date(),
                                  finalDate.date())

def getAvistamientosByCity(analyzer, city):
    """
    Retorna el total de ciudades con avistamientos
    """
    return model.getAvistamientosByCity(analyzer, city)

def get5bestcities(analyzer):
    """
    Retorna las 5 ciudades con más avistamientos
    """
    return model.get5bestcities(analyzer)

def get5bestdurations(analyzer):
    """
    Retorna las 5 ciudades con más avistamientos
    """
    return model.get5bestdurations(analyzer)

def getAvistamientosByDuration(analyzer, min, max):
    """
    Retorna las duraciones en un rango de tiempo de los avistamientos 
    """
    return model.getAvistamientosByDuration(analyzer, min, max)
