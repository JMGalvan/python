# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Processes
from processes import advanced_information
from processes import common
from processes import files
from processes import launchs
from processes import station_requests
from processes import translate

# Validations
from validations.integer_validations import  isValidInteger
from validations.integer_validations import  valueIntegerIncluded

# Variables
configurationData = {}

#
#   loadConfigurationData: Carga la configuración establecida en el fichero settings.json
#
def loadConfigurationData() -> None:
    globals()['configurationData'] = files.readFile('system_data/data/settings.json')
    translate.loadProperties(getLanguage())

#
#   openMenu: Carga el menú de configuración
#
def openMenu() -> None:
    menuOptions = [
        translate.getValue('SETTING_MENU.EXIT'),
        translate.getValue('SETTING_MENU.CHANGE_LANGUAGE')
        ]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    if selectedOption != 0:
        if selectedOption == 1:
            newLanguage = translate.openMenu()
            if len(newLanguage) > 0:
                setLanguage(newLanguage)
        openMenu()

#
#   setDay: Modifica el parámetro __day
#   @param newDay (Integer): nuevo valor para __day
#
def setDay(newDay: int) -> None:
    if isValidInteger(newDay):
        globals()['configurationData']['day'] = int(newDay)
    else:
        print("Error - Invalid data type. Expected data type: integer")
    
#
#   getDay: Obtiene el valor de __day
#   @return (Integer)
#
def getDay() -> int:
    return globals()['configurationData']['day']


#
#   setLanguage: Modifica el parámetro __language
#   @param newLanguage (String): nuevo valor para __language
#
def setLanguage(newLanguage: str) -> None:
    if type(newLanguage) == str:
        globals()['configurationData']['language'] = newLanguage
        saveConfiguration()
    else:
        print("Error - Invalid data type. Expected data type: string")
    
#
#   getLanguage: Obtiene el valor de __language
#   @return string
#
def getLanguage() -> str:
    return globals()['configurationData']['language']

#
#   saveConfiguration: Realiza el guardado de la configuración
#
def saveConfiguration() -> None:
    files.writeFile('system_data/data/settings.json', globals()['configurationData'])

#
#   incrementDays: Incrementa los días indicados
#
def incrementDays() -> None:
    days: int = getDays()
    for day in range(days):
        setDay(getDay() + 1)
        print("\n -------------------")
        print("\n# " + str(getDay()))
        advanced_information.loadRecordToday()
        station_requests.decrementDayRequests()
        launchs.decrementDayLaunchs()
        advanced_information.saveRecords()
        saveConfiguration()

#
#   getDays: Pide al usuario el número de días
#   @return (Integer)
#
def getDays() -> int:
    days = input(translate.getValue('SETTING_MENU.REQUEST_DAYS') + ": ")
    while not valueIntegerIncluded(days, 1, 366):
        print(translate.getValue('SETTING_MENU.REQUEST_DAYS_ERROR'))
        days = input(translate.getValue('SETTING_MENU.REQUEST_DAYS') + ": ")
    return int(days)