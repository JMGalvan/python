# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Extras
import functools

# Processes
from processes import advanced_information
from processes import common
from processes import files
from processes import translate

# Classes
from classes.record import Record
from classes.request import Request

# Validations
from validations.float_validations import  valueFloatIncluded
from validations.integer_validations import  valueIntegerIncluded

# Variables
__requests: [Request] = []

#
#   openMenu: Carga el menú de peticiones a la estación
#
def openMenu() -> None:
    menuOptions = [
        translate.getValue('STATION_REQUESTS_MENU.EXIT'),
        translate.getValue('STATION_REQUESTS_MENU.NEW_REQUEST'),
        translate.getValue('STATION_REQUESTS_MENU.SEE_REQUESTS')]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    if selectedOption != 0:
        if selectedOption == 1:
            addNewRequest()
        elif selectedOption == 2:
            printRawRequestsList()
        openMenu()

#
#   loadRequests: Carga la lista de peticiones a la estación del fichero requests.json
#
def loadRequests() -> None:
    setRequests(list(map(lambda requests: Request(requests['id'], requests['weight'], requests['description'], requests['time_max'], requests['dispatched']), files.readFile('system_data/data/requests.json')['requests'])))

#
#   setRequests: Modifica el parámetro __requests
#   @param requests ([Request]): Lista de peticiones
#
def setRequests(requests: [Request]) -> None:
    globals()['__requests'] = requests
    
#
#   getRequests: Obtiene el valor de __requests
#   @return ([Request])
#
def getRequests() -> [Request]:
    return globals()['__requests'] 

#
#   getRawRequests: Devuelve las peticiones sin procesar
#   @return ([Request])
#
def getRawRequests() -> [Request]:
    return list(filter(lambda request: not request.getDispatched() and request.getTimeMax() > 0, getRequests()))

#
#   printRequestsList: Muestra por pantalla la lista de peticiones
#
def printRequestsList() -> None:
    print("***********************")
    for request in getRequests():
        print(request)
    print("\n***********************")

#
#   printRawRequestsList: Muestra por pantalla la lista de peticiones sin procesar
#
def printRawRequestsList() -> None:
    print("***********************")
    for request in getRawRequests():
        print(request)
    print("\n***********************")

#
#   addNewRequest: Agrega una nueva petición a las existentes
#
def addNewRequest() -> None:
    newRequest: Request = Request(getRequestName(), getRequestWeight(), getRequestDescription(), getDays(), False)
    advanced_information.addRecord(Record('INFORMATION_HISTORY.NEW_REQUEST', newRequest.getId()))
    print("\n" + translate.getValue('INFORMATION_HISTORY.NEW_REQUEST') + ": " + newRequest.getId())
    globals()['__requests'].append(newRequest)
    saveRequests()
#
#   getRequestName: Pide al usuario el nombre de la petición
#   @return (String)
#
def getRequestName() -> str:
    requests = list(map(lambda request: request.getId(), getRequests()))
    name = common.cleanText(input(translate.getValue('STATION_REQUESTS_MENU.REQUEST_NAME') + ": "))
    while (len(name) < 3) or (name in requests) or (len(name) > 14):
        print(translate.getValue('STATION_REQUESTS_MENU.REQUEST_NAME_ERROR'))
        name = common.cleanText(input(translate.getValue('STATION_REQUESTS_MENU.REQUEST_NAME') + ": "))
    return name

#
#   getRequestWeight: Pide al usuario el peso de la petición
#   @return (Integer)
#
def getRequestWeight() -> int:
    weight = input(translate.getValue('STATION_REQUESTS_MENU.REQUEST_WEIGHT') + ": ").replace(",", ".")
    while not valueFloatIncluded(weight, 0.001, 100000, 3):
        print(translate.getValue('STATION_REQUESTS_MENU.REQUEST_WEIGHT_ERROR'))
        weight = input(translate.getValue('STATION_REQUESTS_MENU.REQUEST_WEIGHT') + ": ").replace(",", ".")
    return int(float(weight)*1000)

#
#   getRequestDescription: Pide al usuario descripción de la petición
#   @return (String)
#
def getRequestDescription() -> str:
    description = input(translate.getValue('STATION_REQUESTS_MENU.REQUEST_DESCRIPTION') + ": ").strip()
    while (len(description) < 3) or (len(description) > 100):
        print(translate.getValue('STATION_REQUESTS_MENU.REQUEST_DESCRIPTION_ERROR'))
        description = input(translate.getValue('STATION_REQUESTS_MENU.REQUEST_DESCRIPTION') + ": ").strip()
    return description

#
#   getDays: Pide al usuario el número de días
#   @return (Integer)
#
def getDays() -> int:
    days = input(translate.getValue('STATION_REQUESTS_MENU.REQUEST_DAYS') + ": ")
    while not valueIntegerIncluded(days, 1, 366):
        print(translate.getValue('STATION_REQUESTS_MENU.REQUEST_DAYS_ERROR'))
        days = input(translate.getValue('STATION_REQUESTS_MENU.REQUEST_DAYS') + ": ")
    return int(days)

#
#   saveRequests: Realiza el guardado de las peticiones
#
def saveRequests() -> None:
    files.writeFile('system_data/data/requests.json', {
        "requests": list(map(lambda request: request.getRequestData(), getRequests()))
    })

#
#   sortRequests: Ordena las peticiones por fecha de menor a mayor y en caso de tener la misma fecha ordena la petición por peso de mayor a menor
#   @param actual (Request): Constante de peticioens
#   @param nextElement (Request): Siguiente petición
#   @return [Request]
#
def sortRequests(actual: Request, nextElement: Request) -> [Request]:
    if type(actual) is Request:
        actual = [actual]
    index = 0
    while index < len(actual) and (
        nextElement.getTimeMax() > actual[index].getTimeMax() or (
        nextElement.getTimeMax() == actual[index].getTimeMax() and nextElement.getWeight() <= actual[index].getWeight())):
            index +=  1

    actual.insert(index, nextElement)
    return actual

#
#   decrementDayRequests: Decrementa en un día el tiempo máximo de entrega de las peticiones
#
def decrementDayRequests() -> None:
    for request in getRequests():
        if request.getTimeMax() > 0:
            request.setTimeMax(request.getTimeMax() - 1)
            if request.getTimeMax() == 0 and not request.getDispatched():
                print(translate.getValue('INFORMATION_HISTORY.EXPIRED_REQUEST') + ": " + request.getId())
                advanced_information.addRecord(Record('INFORMATION_HISTORY.EXPIRED_REQUEST', request.getId()))
                    
    saveRequests()
            