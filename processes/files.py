# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Processes
from processes import translate
from processes import common

# Extras
import json
import os
import sys
import shutil

#
#   openMenu: Carga el menú de configuración
#
def openMenu() -> None:
    menuOptions = [
        translate.getValue('FILES_MENU.EXIT'),
        translate.getValue('FILES_MENU.LOAD_DATA'),
        translate.getValue('FILES_MENU.SAVE_DATA'),
        translate.getValue('FILES_MENU.RESET_DATA')
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

def loadLocalData() -> None:
    files: [str] =  getListDir('system_data/save_files')
    if len(files) > 0:
        for nameFile in files:
            print('fileName: ' + nameFile)
    else:
        print('No hay datos para cargar')

def saveLocalData()  -> None:
    print('save')

def resetLocalData() -> None:
    if securityDataMessage():
        resetData()
        loadData('clean_data', 'system_data')

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
    
def createDir(directoryRoute: str) -> None:
    try:
        os.mkdir(directoryRoute)
    except OSError:
        print ('Error creating new directory: ' + directoryRoute)

def securityDataMessage() -> bool:
    print('\n'+translate.getValue('FILES_MENU.ALERT_MESSAGE'))
    menuOptions = [
        translate.getValue('FILES_MENU.NO'),
        translate.getValue('FILES_MENU.YES')
        ]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    return False if selectedOption == 0 else True