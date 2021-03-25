# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
#
#   isValidInteger: Comprueba si el valor es un número entero, en caso de no serlo,
#   revisa si se puede transformar a entero
#   @param value (Integer): Valor a revisar
#   @return boolean
#
def isValidInteger(value):
    if type(value) != int:
            try:
                if int(value) or int(value) == 0 :
                    return True
            except:
                return False
    else:
        return True

#
#   valueIntegerIncluded: Comprueba si el valor recibido, está comprendido entre el valor mínimo y máximo establecido.
#   @param value (Integer): Valor que se tiene que validar.
#   @param minValue (Integer): Valor mínimo válido, el valor introducido por el usuario debe de ser mayor o igual a este.
#   @param maxValue (Integer): Valor máximo válido, el valor introducido por el usuario debe de ser menor a este.
#   @return Boolean
#
def valueIntegerIncluded(value, minValue, maxValue):
    if isValidInteger(value) and isValidInteger(minValue) and isValidInteger(maxValue):
        return int(value) >= int(minValue) and int(value) < int(maxValue)
    else:
        return False