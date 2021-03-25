# -*- coding: utf-8 -*-
"""
@author: José Manuel Galván Díaz
@course: 08GIIN Metodología de Programación

"""
from processes.configuration import loadConfigurationData
from processes.types_rockets import loadRockets
from processes.station_requests import loadRequests
from processes.launchs import loadLaunchs
from processes.advanced_information import loadRecordToday
from processes.main import openMenu

loadConfigurationData()
loadRockets()
loadRequests()
loadLaunchs()
loadRecordToday()
openMenu()

        