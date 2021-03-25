# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Processes
from processes import common
from processes import configuration
from processes import files

# Variables
properties = {}

#
#   loadProperties: Carga los textos que van a ser utilizadas en la aplicación, en base al idioma.
#   @param language (String): Indica el idioma seleccionado. Actualmente acepta los valores 'es' y 'en'
#
def loadProperties(language: str) -> None:
    if language == 'es':
        globals()['properties'] = files.readFile('system_data/languages/es.json')
    elif language == 'en':
        globals()['properties'] = files.readFile('system_data/languages/en.json')
    else:
        print("Error - Invalid value. Expected values: ['es', 'en']")

#
#   getValue: Busca dentro de "properties" el valor definido para la ruta indicada.
#   @param key (String): Ruta del texto que se quiere obtener.
#   @return String
#
def getValue(key: str) -> str:
    try:
        keys = key.split('.')
        value = properties
        for key in keys:
            value = value[key]
        if type(value) is str:
            return value
        else: 
            return 'Unknown value'
    except:
        return 'Unknown value'

#
#   openMenu: Pide al usuario que seleccione un idioma y carga las traducciones.
#   @return string
#
def openMenu() -> str:
    menuOptions = [
        getValue('SETTING_MENU.EXIT'),
        getValue('COMMON.LANGUAGES.ES'),
        getValue('COMMON.LANGUAGES.EN')
        ]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    if selectedOption != 0:
        if selectedOption == 1:
            loadProperties('es')
            return 'es'
            file.writeFile()
        elif selectedOption == 2:
            loadProperties('en')
            return 'en'
    else:
        return ''