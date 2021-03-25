# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
# Processes
from processes import advanced_information
from processes import common
from processes import configuration
from processes import launchs
from processes import station_requests
from processes import translate
from processes import types_rockets

#
#   openMenu: Carga el menú principal
#
def openMenu() -> None:
    print("\n" + translate.getValue('MAIN_MENU.TODAY') + ": " + str(configuration.getDay()))
    menuOptions = [
        translate.getValue('MAIN_MENU.EXIT'),
        translate.getValue('MAIN_MENU.TYPES_OF_ROCKETS'),
        translate.getValue('MAIN_MENU.STATION_REQUESTS'),
        translate.getValue('MAIN_MENU.RELEASES_AVAILABLE'),
        translate.getValue('MAIN_MENU.ASSIGN'),
        translate.getValue('MAIN_MENU.DAYS'),
        translate.getValue('MAIN_MENU.ADVANCED_INFORMATION'),
        translate.getValue('MAIN_MENU.SETTING')
        ]
    common.printMenu(menuOptions)
    selectedOption = common.requestOptionInteger(0, len(menuOptions))
    if selectedOption != 0:
        if selectedOption == 1:
            types_rockets.openMenu()
        elif selectedOption == 2:
            station_requests.openMenu()
        elif selectedOption == 3:
            launchs.openMenu()
        elif selectedOption == 4:
            launchs.assignRequestsToLaunchs()
        elif selectedOption == 5:
            configuration.incrementDays()
        elif selectedOption == 6:
            advanced_information.openMenu()
        elif selectedOption == 7:
            configuration.openMenu()
        openMenu()
    else:
        print(translate.getValue('COMMON.EXIT'))
    


    