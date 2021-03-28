# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Processes
from processes import translate
from processes import common
from processes import configuration
from processes import types_rockets
from processes import station_requests
from processes import launchs
from processes import advanced_information

# Extras
import json
import os
import sys
import shutil

#
#   loadAllData: Carga los datos en la aplicación
#
def loadAllData() -> None:
    configuration.loadConfigurationData()
    types_rockets.loadRockets()
    station_requests.loadRequests()
    launchs.loadLaunchs()
    advanced_information.loadRecordToday()

#
#   openMenu: Carga el menú de configuración
#
def openMenu() -> None:
    menuOptions = [
        translate.getValue('FILES_MENU.EXIT'),
        translate.getValue('FILES_MENU.LOAD_DATA'),
        translate.getValue('FILES_MENU.SAVE_DATA'),
        translate.getValue('FILES_MENU.RESET_DATA'),
        translate.getValue('FILES_MENU.DELETE_DATA')
        ]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    if selectedOption != 0:
        if selectedOption == 1:
            loadLocalData()
        elif selectedOption == 2:
            saveLocalData()
        elif selectedOption == 3:
            resetLocalData()
        elif selectedOption == 4:
            deleteLocalData()
        openMenu()

#
#   readFile: Obtiene los datos del fichero indicado
#   @param routeFile (String): ruta del fichero
#   @return dictionary
#
def readFile(routeFile: str) -> dict:
    try:
        with open(routeFile, encoding='utf-8') as file:
            return json.load(file)
    except:
        if (routeFile == 'system_data/data/settings.json'):
            resetData()
            loadData('clean_data', 'system_data')
            return readFile(routeFile)
        
        print("Error - No such file or directory: '" + routeFile + "'")
        sys.exit()

#
#   writeFile: Guarda los datos en el fichero indicado
#   @param routeFile (String): ruta del fichero
#   @param data: información a guardar
#
def writeFile(routeFile: str, data: dict) -> None:
    try:
        with open(routeFile, 'w') as file:
            json.dump(data, file, indent=4)
    except BaseException as e:
        print("Error - '" + e.__doc__ + "'")

#
#   existsFile: Comprueba si el fichero existe
#   @param routeFile (String): ruta del fichero
#   @return (Boolean)
#
def existsFile(routeFile: str) -> bool:
    return os.path.isfile(routeFile)

#
#   getListDir: Devuelve el nombre de los elementos localizados dentro de la ruta
#   @param routeFile (String): ruta para revisar
#   @return ([String])
#
def getListDir(routeFile: str) -> [str]:
    return os.listdir(routeFile)

#
#   loadLocalData: Carga los datos seleccionados en la memoria actual
#
def loadLocalData() -> None:
    files: [str] =  getListDir('system_data/save_files')
    if len(files) > 0:
        print('\n'+translate.getValue('FILES_MENU.LOAD_DATA_MESSAGE'))
        common.printMenu(files, False)
        selectedOption = common.requestOptionInteger(0, len(files))
        if securityDataMessage():
            resetData()
            loadData(files[selectedOption])
    else:
        print('\n'+translate.getValue('FILES_MENU.DATA_NOT_FOUND'))

#
#   deleteLocalData: Elimina los datos de la memoria actual
#
def deleteLocalData() -> None:
    files: [str] =  getListDir('system_data/save_files')
    if len(files) > 0:
        print('\n'+translate.getValue('FILES_MENU.DELETE_DATA_MESSAGE'))
        common.printMenu(files, False)
        selectedOption = common.requestOptionInteger(0, len(files))
        if securityDataMessage():
            resetData('system_data/save_files/' + files[selectedOption])
            print('\n'+translate.getValue('FILES_MENU.DELETE_DATA_COMPLETE'))
    else:
        print('\n'+translate.getValue('FILES_MENU.DATA_NOT_FOUND'))

#
#   saveLocalData: Guarda los datos de la memoria actual en un espacio existente o nuevo
#
def saveLocalData()  -> None:
    files: [str] =  getListDir('system_data/save_files')
    print('\n'+translate.getValue('FILES_MENU.SAVE_DATA_MESSAGE'))
    optionsMenu = [translate.getValue('FILES_MENU.NEW_SLOT')] + files
    common.printMenu(optionsMenu)
    selectedOption = common.requestOptionInteger(0, len(optionsMenu))
    if selectedOption == 0:
        saveData(requestSaveName())
    else:
        resetData('system_data/save_files/' + optionsMenu[selectedOption])
        saveData(optionsMenu[selectedOption])

#
#   resetLocalData: Reinicia los datos de la memoria actual
#
def resetLocalData() -> None:
    if securityDataMessage():
        resetData()
        loadData('clean_data', 'system_data')

#
#   resetData: Reinicia los datos
#
def resetData(src="system_data/data") -> None:
    if os.path.exists(src):
        files = getListDir(src)
        for fileName in files:
            srcAux = src + '/' + fileName
            if os.path.isdir(srcAux):
                resetData(srcAux)
            else:
                try:
                    os.remove(srcAux)
                except OSError:
                    print ('- Error delete file: ' + fileName)
        os.rmdir(src)

#
#   saveData: Guarda los datos
#
def saveData(saveName, src="system_data/data", dst="system_data/save_files") -> None:
    dst = dst + '/' + saveName
    createDir(dst)
    lista = getListDir(src)
    for fileName in lista:
        s = src + '/' + fileName
        d = dst + '/' + fileName
        if os.path.isdir(s):
            saveData(fileName, src+ '/' + fileName, dst)
        else:
            try:
                shutil.copy2(s, d)
            except OSError:
                print ('- Error saving file: ' + fileName)
            else:
                print('- File save completed: ' + fileName)

#
#   loadData: Carga los datos
#
def loadData(saveName,  src="system_data/save_files", dst="system_data/data") -> None:
    src = src + '/' + saveName
    createDir(dst)
    lista = getListDir(src)
    for fileName in lista:
        s = src + '/' + fileName
        d = dst + '/' + fileName
        if os.path.isdir(s):
            saveData(fileName, src + '/' + fileName, dst)
        else:
            try:
                shutil.copy2(s, d)
            except OSError:
                print ('- Error loading file: ' + fileName)
            else:
                print('- File load completed: ' + fileName)
    loadAllData()

#
#   createDir: Crea un directorio
#
def createDir(directoryRoute: str) -> None:
    try:
        os.mkdir(directoryRoute)
    except OSError:
        print ('Error creating new directory: ' + directoryRoute)

#
#   securityDataMessage: Muestra un mensaje de advertencia al usuario
#
def securityDataMessage() -> bool:
    print('\n'+translate.getValue('FILES_MENU.ALERT_MESSAGE'))
    menuOptions = [
        translate.getValue('FILES_MENU.NO'),
        translate.getValue('FILES_MENU.YES')
        ]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    return False if selectedOption == 0 else True

#
#   requestSaveName: Pide al usuario el nombre del guardado
#   @return (String)
#
def requestSaveName() -> str:
    files: [str] =  getListDir('system_data/save_files')
    name = common.cleanText(input(translate.getValue('FILES_MENU.SAVE_NAME') + ": "))
    while (len(name) < 3) or (name in files) or (len(name) > 14):
        print(translate.getValue('FILES_MENU.SAVE_NAME_ERROR'))
        name = common.cleanText(input(translate.getValue('FILES_MENU.SAVE_NAME') + ": "))
    return name