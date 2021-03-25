# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Extras
import functools 

# Processes
from processes import common
from processes import configuration
from processes import files
from processes import launchs
from processes import station_requests
from processes import translate

# Classes
from classes.record import Record

# Validations
from validations.integer_validations import  valueIntegerIncluded

# Variables
__records: [Record] = []

#
#   openMenu: Carga el menú de información avanzada
#
def openMenu() -> None:
    menuOptions = [
        translate.getValue('ADVANCED_INFORMATION_MENU.EXIT'),
        translate.getValue('ADVANCED_INFORMATION_MENU.REQUESTS'),
        translate.getValue('ADVANCED_INFORMATION_MENU.LAUNCHS'),
        translate.getValue('ADVANCED_INFORMATION_MENU.RECORD')]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    if selectedOption != 0:
        if selectedOption == 1:
            station_requests.printRequestsList()
        elif selectedOption == 2:
            launchs.printLaunchsList()
        elif selectedOption == 3:
            showRecord()
        openMenu()

#
#   showRecord: Solicita un día para mostrar por pantalla su registro
#
def showRecord() -> None:
    day = input("\n" + translate.getValue('ADVANCED_INFORMATION_MENU.SELECTED_DAY') + "(0" + ("" if configuration.getDay() == 0 else " - " + str(configuration.getDay())) + ")" + ": ")
    while not valueIntegerIncluded(day, 0, (configuration.getDay() + 1)):
        day = input("\n" + translate.getValue('ADVANCED_INFORMATION_MENU.SELECTED_DAY_ERROR') + ": ")
    
    printRecords(list(map(lambda record: Record(record['id'], record['value']), loadRecordDay(int(day)))))

#
#   printRecords: Muestra por pantalla los registros
#   @param record ([Record]): Registros
#
def printRecords(records: [Record]) -> None:
    print("***********************")
    if len(records) > 0:
        for record in records:
            print(record)
    else:
        print(translate.getValue('ADVANCED_INFORMATION_MENU.NO_RECORDS'))
    print("\n***********************")


#
#   loadRockets: Carga la lista de cohetes del fichero rockets.json
#
def loadRecordToday() -> None:
    setRecords(list(map(lambda record: Record(record['id'], record['value']), loadRecordDay(configuration.getDay()))))

#
#   loadRecordDay: Carga los registros del día indicado
#   @param day (Integer): Día
#
def loadRecordDay(day: int) -> [Record]:
    routeFile: str = 'system_data/records/' + str(day) + '.json'
    if (files.existsFile(routeFile)):
        return files.readFile(routeFile)['records']
    else:
        files.writeFile(routeFile, {
            "records": []
        })
        return []

#
#   setRecords: Modifica el parámetro __records
#   @param records ([Record]): Lista de peticiones
#
def setRecords(records: [Record]) -> None:
    globals()['__records'] = records
    
#
#   getRecords: Obtiene el valor de __records
#   @return ([Request])
#
def getRecords() -> [Record]:
    return globals()['__records'] 

#
#   addRecord: Agrega un nuevo registro
#   @param record (Record): Nuevo registro
#
def addRecord(record: Record) -> None:
    globals()['__records'].append(record)
    saveRecords()

#
#   saveRecords: Realiza el guardado de los cohetes
#
def saveRecords() -> None:
    files.writeFile('system_data/records/' + str(configuration.getDay()) + '.json', {
        "records": list(map(lambda record: record.getRecordData(), getRecords()))
    })