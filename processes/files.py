# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Extras
import json
import os
import sys

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
    