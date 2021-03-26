# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Extras
import functools 
from datetime import datetime

# Processes
from processes import advanced_information
from processes import common
from processes import files
from processes import station_requests
from processes import translate
from processes import types_rockets

# Classes
from classes.launch import Launch
from classes.record import Record
from classes.request import Request
from classes.rocket import Rocket

# Validations
from validations.integer_validations import  valueIntegerIncluded

# Variables
__launchs: [Launch] = []

#
#   openMenu: Carga el menú de lanzamientos
#
def openMenu() -> None:
    menuOptions = [
        translate.getValue('LAUNCHS_MENU.EXIT'),
        translate.getValue('LAUNCHS_MENU.NEW_LAUNCH'),
        translate.getValue('LAUNCHS_MENU.SEE_LAUNCHS')
        ]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    if selectedOption != 0:
        if selectedOption == 1:
            addNewLaunch()
        elif selectedOption == 2:
            printLaunchsList()
        openMenu()

#
#   loadLaunchs: Carga la lista de lanzamientos del fichero launchs.json
#
def loadLaunchs() -> None:
    setLaunchs(list(map(lambda launch: Launch(launch['id'], launch['id_rocket'], launch['max_weight'], launch['shipload'], launch['requests'], launch['time'], launch['dispatched']), files.readFile('system_data/data/launchs.json')['launchs'])))
#
#   setLaunchs: Modifica el parámetro __launchs
#   @param requests ([Launch]): Lista de lanzamientos
#
def setLaunchs(launchs: [Launch]) -> None:
    globals()['__launchs'] = launchs
    
#
#   getLaunchs: Obtiene el valor de __launchs
#   @return ([Launch]): Lista de lanzamientos
#
def getLaunchs() -> [Launch]:
    return globals()['__launchs'] 

#
#   getRawLaunchs: Devuelve los lanzamientos sin procesar
#   @return ([Request])
#
def getRawLaunchs() -> [Launch]:
    return list(filter(lambda launch: not launch.getDispatched() and launch.getTime() > 0, getLaunchs()))

#
#   printLaunchsList: Muestra por pantalla la lista de lanzamientos
#
def printLaunchsList() -> None:
    print("***********************")
    for launch in getRawLaunchs():
        print(launch)
    print("\n***********************")

#
#   addNewLaunch: Agrega un nuevo lanzamiento a los existentes
#
def addNewLaunch() -> None:
    rocketSelected: Rocket = types_rockets.getTypeRocket()
    newLaunch: Launch = Launch(generateLaunchId(), rocketSelected.getId(), rocketSelected.getShipload(), 0, [], getDays(), False)
    advanced_information.addRecord(Record('INFORMATION_HISTORY.NEW_LAUNCH', newLaunch.getId()))
    print("\n" + translate.getValue('INFORMATION_HISTORY.NEW_LAUNCH') + ": " + newLaunch.getId())
    globals()['__launchs'].append(newLaunch)
    saveLaunchs()

#
#   generateLaunchId: Genera el identificador del lanzamiento a partir de la fecha actual
#   @return (String)
#
def generateLaunchId() -> str:
    launchId = datetime.now().strftime("%Y%m%d%H%M%S")
    while launchId in list(map(lambda launch: launch.getId(), getLaunchs())):
        launchId = datetime.now().strftime("%Y%m%d%H%M%S")
    return launchId

#
#   getDays: Pide al usuario el número de días
#   @return (Integer)
#
def getDays() -> int:
    days = input(translate.getValue('LAUNCHS_MENU.REQUEST_DAYS') + ": ")
    while not valueIntegerIncluded(days, 1, 366):
        print(translate.getValue('LAUNCHS_MENU.REQUEST_DAYS_ERROR'))
        days = input(translate.getValue('LAUNCHS_MENU.REQUEST_DAYS') + ": ")
    return int(days)


#
#   saveLaunchs: Realiza el guardado de los lanzamientos
#
def saveLaunchs() -> None:
    files.writeFile('system_data/data/launchs.json', {
        "launchs": list(map(lambda launch: launch.getLaunchData(), getLaunchs()))
    })

#
#   assignRequestsToLaunchs: Asigna las peticiones a los lanzamientos
#
def assignRequestsToLaunchs() -> None:
    advanced_information.addRecord(Record('INFORMATION_HISTORY.ASSIGNED', ""))
    # Obtenemos las peticiones sin procesar y las ordenamos
    requestSorted: [Request] = station_requests.getRawRequests()
    requestSorted = requestSorted if len(requestSorted) < 2 else functools.reduce(lambda actual, nextElement : station_requests.sortRequests(actual, nextElement), station_requests.getRawRequests())

    # Obtenemos los lanzamientos sin procesar y los ordenamos
    launchsSorted: [Launch] = getRawLaunchs()
    launchsSorted = launchsSorted if len(launchsSorted) < 2 else functools.reduce(lambda actual, nextElement : sortLaunchs(actual, nextElement), launchsSorted)

    indexLaunch = 0

    # Revisamos cada lanzamiento, deteniendo el flujo cuando no queden peticiones por asignar
    while indexLaunch < len(launchsSorted) and len(requestSorted) > 0:
        indexRequest = 0

        # Revisamon cada petición, deteniendo el flujo cuando el lanzamiento actual no tenga espacio disponible
        while indexRequest < len(requestSorted) and (launchsSorted[indexLaunch].getMaxWeight() - launchsSorted[indexLaunch].getShipload()) != 0:
            # Comprobamos si la petición se puede asignar al lanzamiento y/o la fecha de lanzamiento sea superior a la fecha de la petición
            if (launchsSorted[indexLaunch].getMaxWeight() - (launchsSorted[indexLaunch].getShipload() + requestSorted[indexRequest].getWeight())) >= 0  and launchsSorted[indexLaunch].getTime() <= requestSorted[indexRequest].getTimeMax():
                # Guardamos la nueva carga del lanzamiento
                launchsSorted[indexLaunch].setShipload(launchsSorted[indexLaunch].getShipload() + requestSorted[indexRequest].getWeight())

                # Asignamos la petición al lanzamiento
                requestsAux = launchsSorted[indexLaunch].getRequests()
                requestsAux.append(requestSorted[indexRequest].getId())
                launchsSorted[indexLaunch].setRequests(requestsAux)

                # Cambiamos el estado de la petición a asignada
                advanced_information.addRecord(Record('INFORMATION_HISTORY.REQUEST_IN_TRANSIT', requestSorted[indexRequest].getId() ))
                requestSorted[indexRequest].setDispatched(True)

                # Registramos en que lanzamiento se ha asignado la petición
                advanced_information.addRecord(Record('INFORMATION_HISTORY.REQUEST_ASSIGNED_LAUNCH', requestSorted[indexRequest].getId() + " -> " + launchsSorted[indexLaunch].getId()))
                print(translate.getValue('LAUNCHS_MENU.ASSIGNED_REQUEST').translate(str.maketrans({'X': launchsSorted[indexLaunch].getId(),'Y': requestSorted[indexRequest].getId()})))

                # Registramos cuando la carga del lanzamiento se completa
                if (launchsSorted[indexLaunch].getMaxWeight() == launchsSorted[indexLaunch].getShipload()):
                    advanced_information.addRecord(Record('INFORMATION_HISTORY.SHIPLOAD_COMPLETE', launchsSorted[indexLaunch].getId()))

            indexRequest += 1
        # Obtenemos las peticiones sin procesar
        requestSorted = list(filter(lambda request: not request.getDispatched(), requestSorted))
        indexLaunch += 1
    
    # Se muestran por pantalla las peticiones que no han podido ser asignadas
    if len(requestSorted) > 0:
        print("***********************")
        for request in requestSorted:
            print(translate.getValue('LAUNCHS_MENU.UNASSIGNED_REQUEST') + ": " + request.getId())
        print("\n***********************")
    
    saveLaunchs()
    station_requests.saveRequests()
    

#
#   sortLaunchs: Ordena los lanzamientos por fecha de menor a mayor y en caso de tener la misma fecha ordena el lanzamiento por carga disponible de menor a mayor
#   @param actual (Launch): Constante de lanzamientos
#   @param nextElement (Launch): Siguiente lanzamiento
#   @return [Launch]
#
def sortLaunchs(actual: Launch, nextElement: Launch) -> [Launch]:
    if type(actual) is Launch:
        actual = [actual]
    if nextElement:
        index = 0
        while index < len(actual) and (
            nextElement.getTime() > actual[index].getTime() or (
            nextElement.getTime() == actual[index].getTime() and (nextElement.getMaxWeight() - nextElement.getShipload()) >= (actual[index].getMaxWeight() - actual[index].getShipload()))):
                index +=  1

        actual.insert(index, nextElement)
    return actual

#
#   decrementDayLaunchs: Decrementa los días de los lanzamientos, en caso de no tener peticiones asignadas, el lanzamiento se cancela
#
def decrementDayLaunchs() -> None:
    for launch in getLaunchs():
        if launch.getTime() > 0:
            launch.setTime(launch.getTime() - 1)
            if not launch.getDispatched():
                if len(launch.getRequests()) > 0:
                    print(translate.getValue('INFORMATION_HISTORY.LAUNCH_IN_TRANSIT') + ": " + launch.getId())
                    advanced_information.addRecord(Record('INFORMATION_HISTORY.LAUNCH_IN_TRANSIT', launch.getId()))
                    launch.setDispatched(True)
                else:
                    print(translate.getValue('INFORMATION_HISTORY.CANCEL_LAUNCH') + ": " + launch.getId())
                    advanced_information.addRecord(Record('INFORMATION_HISTORY.CANCEL_LAUNCH', launch.getId()))
                    launch.setTime(0)
            if launch.getTime() == 0 and launch.getDispatched():
                advanced_information.addRecord(Record('INFORMATION_HISTORY.SUCCESSFUL_LAUNCH', launch.getId()))
                print(translate.getValue('INFORMATION_HISTORY.SUCCESSFUL_LAUNCH') + ": " + launch.getId())
                for request in station_requests.getRequests():
                    if request.getId() in launch.getRequests():
                        request.setTimeMax(0)
                        advanced_information.addRecord(Record('INFORMATION_HISTORY.SUCCESSFUL_REQUEST', request.getId()))
                        print(translate.getValue('INFORMATION_HISTORY.SUCCESSFUL_REQUEST') + ": " + request.getId())
    saveLaunchs()
    station_requests.saveRequests()
            