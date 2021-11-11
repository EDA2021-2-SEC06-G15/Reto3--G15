"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


UFOSfile = 'UFOS//UFOS-utf8-small.csv'
cont = None



# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de avistamientos")
    print("3- Consultar los avistamientos en una ciudad")
    print("4- Contar los avistamientos por duración")
    print("5- Contar avistamientos por Hora/Minutos del día")
    print("6- Contar los avistamientos en un rango de fechas")
    print("7- Contar los avistamientos de una Zona Geográfica")
    print("8- Visualizar los avistamientos de una zona geográfica.")
    print("0- Salir")
    print("*******************************************")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        start_time = time.process_time()
        print("\nCargando información de los avistamientos ....")
        controller.loadData(cont, UFOSfile)
        print('avistamientos cargados: ' + str(controller.avistamientosSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)  
        print("Tiempo de ejecución: "+str(elapsed_time_mseg))

    elif int(inputs[0]) == 3:
        city = input("Ingrese la ciudad: ")
        print("\nBuscando avistamientos en la ciudad de: " + str(city))
        cities = controller.citySize(cont)
        print("\nTotal de ciudades con avisamientos: " + str(cities))
        print("-----------------------------------------")
        print("\nTop 5 ciudades con más avistamientos: " )
        print("-----------------------------------------")
        controller.get5bestcities(cont)
        controller.getAvistamientosByCity(cont, city)
        
        
    elif int(inputs[0]) == 4:
        min = input("Ingrese el limite inferior de segundos: ")
        max = input("Ingrese el limite superior de segundos: ")
        duraciones = controller.durationSize(cont)
        print("\nTotal de diferentes duraciones de avisamientos " + str(duraciones))
        controller.get5bestdurations(cont)
        total = controller.getAvistamientosByDuration(cont, min, max)
        print("\nTotal de avistamientos en el rango de tiempos: " + str(total))
        print("\nLos primeros 3 y ultimos 3 avistamientos en el rango de duración dado son: ")

     
    elif int(inputs[0]) == 5:
        hora1 = input("Hora Inicial (hh:mm:ss): ")
        hora2 = input("Hora Final (hh:mm:ss): ")
        horas = controller.TimeSize(cont)
        print("\nTotal de diferentes horas de avisamientos " + str(horas))
        
        print("\nTotal de diferentes horas de avisamientos " + str(horas))
    
    elif int(inputs[0]) == 6:
        print("\nBuscando avistamientos en un rango de fechas: ")
        initialDate = input("Fecha Inicial (YYYY-MM-DD): ")
        finalDate = input("Fecha Final (YYYY-MM-DD): ")
        cant = controller.dateSize(cont)
        print("\nTotal de diferentes fechas de avistamientos  " + str(cant))
        oldest = controller.older(cont)
        total = controller.getAvistamientosByRange(cont, initialDate, finalDate)
        print("\nTotal de avistamientos en el rango de fechas: " + str(total))
    
    elif int(inputs[0]) == 7:

        longitudes = controller.LongitudSize(cont)
        print("\nTotal de diferentes longitudes de avisamientos " + str(longitudes))
        longitud1 = input("Longitud Inicial: ")
        longitud2 = input("Longitud Final: ")
        latitud1 = input("Latitud Inicial: ")
        latitud2 = input("Latitud Final: ")
        avistamientos = controller.getavistamientos(cont, longitud1, longitud2, latitud1, latitud2)
    
    elif int(inputs[0]) == 8:
        pass

    else:
        sys.exit(0)
sys.exit(0)
