# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Extras
import re

# Processes
from processes import translate

# Validations
from validations.integer_validations import  valueIntegerIncluded

#
#   printMenu: Imprime un menú con las opciones indicadas
#   @param options ([String]): Lista de códigos de referencia para las opciones del menú
#
def printMenu(options: [str], exitMode = True) -> None:
    if len(options) > 0:
        print("-----------------------")
        if not exitMode:
            print("0) " + options[0])
        if len(options) > 1:
            for idx, option in enumerate(options):
                if idx != 0:
                    print(str(idx) + ") " + option)
        if exitMode:
            print("0) " + options[0])
        print("-----------------------")

#
#   requestOptionInteger: Pide al usuario un número entero, comprendido entre dos valores
#   @param minValue (Integer): Valor mínimo válido, el valor introducido por el usuario debe de ser mayor o igual a este.
#   @param maxValue (Integer): Valor máximo válido, el valor introducido por el usuario debe de ser menor a este.
#   @return Integer
#
def requestOptionInteger(minValue: int, maxValue: int) -> int:
    option = input("\n" + translate.getValue('COMMON.CHOOSE_OPTION') + ": ")
    while not valueIntegerIncluded(option, minValue, maxValue):
        option = input("\n" + translate.getValue('COMMON.CHOOSE_VALID_OPTION') + ": ")
    return int(option)

#
#   cleanText: Formatea el texto, eliminando de las vocales los acentos, eliminando los espacios y transformandolo a minúsculas.
#   @param text (String): Texto a tratar
#   @return (String)
#
def cleanText(text: str) -> str:
    return removeAccents(text.replace(" ", "").lower())

#
#   removeAccents: Formatea el texto, eliminando de las vocales los acentos.
#   @param text (String): Texto a tratar
#   @return (String)
#
def removeAccents(text: str) -> str:
    return text.translate(str.maketrans({
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U'
    }))