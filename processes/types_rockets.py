# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Processes
from processes import advanced_information
from processes import common
from processes import files
from processes import translate

# Classes
from classes.record import Record
from classes.rocket import Rocket

# Validations
from validations.integer_validations import  valueIntegerIncluded

# Variables
__rockets: [Rocket] = []

#
#   openMenu: Carga el menú de tipos de cohetes
#
def openMenu() -> None:
    menuOptions = [
        translate.getValue('TYPES_ROCKETS_MENU.EXIT'),
        translate.getValue('TYPES_ROCKETS_MENU.NEW_ROCKET'),
        translate.getValue('TYPES_ROCKETS_MENU.SEE_ROCKETS')
        ]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    if selectedOption != 0:
        if selectedOption == 1:
            addNewRocket()
        elif selectedOption == 2:
            printRocketsList()
        openMenu()

#
#   loadRockets: Carga la lista de cohetes del fichero rockets.json
#
def loadRockets() -> None:
    setRockets(list(map(lambda rocket: Rocket(rocket['id'], rocket['shipload']), files.readFile('system_data/data/rockets.json')['rockets'])))
    
#
#   setRockets: Modifica el parámetro __rockets
#   @param rockets ([Rocket]): Lista de cohetes
#
def setRockets(rockets: [Rocket]) -> None:
    globals()['__rockets'] = rockets
        
    
#
#   getRockets: Obtiene el valor de __rockets
#   @return ([Rocket])
#
def getRockets() -> [Rocket]:
    return globals()['__rockets'] 

#
#   addNewRocket: Agrega un nuevo cohete a los existentes
#
def addNewRocket() -> None:
    newRocket: Rocket = Rocket(requestRocketName(), getRocketOTB())
    advanced_information.addRecord(Record('INFORMATION_HISTORY.NEW_ROCKET', newRocket.getId()))
    print("\n" + translate.getValue('INFORMATION_HISTORY.NEW_ROCKET') + ": " + newRocket.getId())
    globals()['__rockets'].append(newRocket)
    saveRockets()

#
#   requestRocketName: Pide al usuario el nombre del cohete
#   @return (String)
#
def requestRocketName() -> str:
    rockets = list(map(lambda rocket: rocket.getId(), getRockets()))
    name = common.cleanText(input(translate.getValue('TYPES_ROCKETS_MENU.ROCKET_NAME') + ": "))
    while (len(name) < 3) or (name in rockets) or (len(name) > 14):
        print(translate.getValue('TYPES_ROCKETS_MENU.ROCKET_NAME_ERROR'))
        name = common.cleanText(input(translate.getValue('TYPES_ROCKETS_MENU.ROCKET_NAME') + ": "))
    return name

#
#   getRocketOTB: Pide al usuario el peso que puede transportar el cohete
#   @return (Integer)
#
def getRocketOTB() -> int:
    otb = input(translate.getValue('TYPES_ROCKETS_MENU.ROCKET_OTB') + ": ")
    while not valueIntegerIncluded(otb, 1, 100000):
        print(translate.getValue('TYPES_ROCKETS_MENU.ROCKET_OTB_ERROR'))
        otb = input(translate.getValue('TYPES_ROCKETS_MENU.ROCKET_OTB') + ": ")
    return int(otb)*1000


#
#   printRocketsList: Muestra por pantalla la lista de cohetes
#
def printRocketsList() -> None:
    print("***********************")
    for rocket in getRockets():
        print(rocket)
    print("\n***********************")

#
#   saveRockets: Realiza el guardado de los cohetes
#
def saveRockets() -> None:
    files.writeFile('system_data/data/rockets.json', {
        "rockets": list(map(lambda rocket: rocket.getRocketData(), getRockets()))
    })

#
#   getTypeRocket: Pide al usuario que seleccione un tipo de cohete
#   @return (Rocket)
#
def getTypeRocket() -> Rocket:
    print(translate.getValue('TYPES_ROCKETS_MENU.GET_ROCKET_TYPE') + ": ")
    menuOptions = list(map(lambda rocket: rocket.getId() + ": " + str(rocket.getShipload()/1000) + " Kg", getRockets()))
    common.printMenu(menuOptions, False)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    return getRockets()[selectedOption]