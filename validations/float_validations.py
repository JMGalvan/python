# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
#
#   isValidFloat: Comprueba si el valor es un número Real, en caso de no serlo,
#   revisa si se puede transformar a Real
#   @param value (Integer): Valor a revisar
#   @return boolean
#
def isValidFloat(value):
    if type(value) != float and type(value) != int:
            try:
                if float(value) or float(value) == 0 :
                    return True
            except:
                return False
    else:
        return True

#
#   valueFloatIncluded: Comprueba si el valor recibido, está comprendido entre el valor mínimo y máximo establecido.
#   @param value (Float): Valor que se tiene que validar.
#   @param minValue (Float): Valor mínimo válido, el valor introducido por el usuario debe de ser mayor o igual a este.
#   @param maxValue (Float): Valor máximo válido, el valor introducido por el usuario debe de ser menor a este.
#   @param decimals (Integer): Número máximo de decimales.
#   @return Boolean
#
def valueFloatIncluded(value, minValue, maxValue, decimals):
    if isValidFloat(value) and isValidFloat(minValue) and isValidFloat(maxValue):
        return float(value) >= float(minValue) and float(value) < float(maxValue) and minDecimals(value, decimals)
    else:
        return False

#
#   minDecimals: Comprueba si el valor recibido, no supera los decimales máximos.
#   @param value (Float): Valor que se tiene que validar.
#   @param decimals (Integer): Número máximo de decimales.
#   @return Boolean
#
def minDecimals(value, decimals):
    numbers = str(value).split(".")
    if len(numbers) == 1:
        return True
    elif len(numbers) > 1:
        return len(numbers[1]) <= decimals