from processes import translate

class Launch:

    #
    #   __init__: Inicializa la clase
    #   @param name (String): Identificador del lanzamiento
    #   @param id_rocket (String): Identificador del cohete del lanzamiento
    #   @param max_weight (Integer): Carga máxima del lanzamiento
    #   @param shipload (Integer): Carga actual del lanzamiento
    #   @param requests ([String]): Peticiones del lanzamiento
    #   @param time (Integer): Tiempo máximo del lanzamiento
    #   @param dispatched (Boolean): Estado del lanzamiento
    #
    def __init__(self, name: str, id_rocket: str, max_weight: int, shipload: int, requests: [str], time: int, dispatched: bool) -> None:
        self.id = name
        self.id_rocket = id_rocket
        self.max_weight = max_weight
        self.shipload = shipload
        self.requests = requests
        self.time = time
        self.dispatched = dispatched
    #
    #   __str__: Retorna los datos del lanzamiento para imprimirlos por pantalla
    #   @return (String)
    #
    def __str__(self) -> str:
        status = ""
        if self.time > 0:
            status = translate.getValue('COMMON.IN_TRANSIT') if self.dispatched else translate.getValue('COMMON.ON_HOLD')
        else:
            status = translate.getValue('COMMON.DELIVERED') if self.dispatched else translate.getValue('COMMON.CANCELED')

        line0 = "\n# " + translate.getValue('COMMON.LAUNCH_CODE') + ": " + self.id
        line1 = "\n  " + translate.getValue('COMMON.ROCKET_TYPE') + ": " + self.id_rocket
        line2 = "\n  " + translate.getValue('COMMON.SHIPLOAD') + ": " + str(int(self.shipload)/1000) + "/" + str(int(self.max_weight)/1000) + " kg." 
        line3 = "\n  " + translate.getValue('COMMON.MAX_DAYS') + ": " +  str(self.time)
        line4 = "\n  " + translate.getValue('COMMON.REQUESTS') + ": "
        line5 = ""
        for request in self.requests:
            line5 = line5 + "\n   - " + request
        line6 = "\n  " + translate.getValue('COMMON.STATUS') + ": " + status

        return line0 + line1 + line2 + line3 + line4 + line5 + line6
    
    #
    #   getId: Retorna el identificador del lanzamiento
    #   @return (String)
    #
    def getId(self) -> str:
        return self.id

    #
    #   setId: Actualiza el identificador del lanzamiento
    #   @param name (String): Nuevo identificador para el lanzamiento
    #
    def setId(self, name: str) -> None:
        self.id = name
    
    #
    #   getIdRocket: Retorna el identificador del cohete del lanzamiento
    #   @return (String)
    #
    def getIdRocket(self) -> str:
        return self.id_rocket

    #
    #   setIdRocket: Actualiza el identificador del cohete del lanzamiento
    #   @param id_rocket (String): Nuevo identificador para el cohete del lanzamiento
    #
    def setIdRocket(self, id_rocket: str) -> None:
        self.id_rocket = id_rocket

    #
    #   getMaxWeight: Retorna el peso máximo del lanzamiento
    #   @return (Integer)
    #
    def getMaxWeight(self) -> int:
        return self.max_weight

    #
    #   setMaxWeight: Actualiza el peso máximo del lanzamiento
    #   @param max_weight (Integer): Nueva peso máximo del lanzamiento
    #
    def setMaxWeight(self, max_weight: int) -> None:
        self.max_weight = max_weight

    #
    #   getShipload: Retorna la carga de la petición
    #   @return (Integer)
    #
    def getShipload(self) -> int:
        return self.shipload

    #
    #   setShipload: Actualiza la carga de la petición
    #   @param shipload (Integer): Nueva carga de la petición
    #
    def setShipload(self, shipload: int) -> None:
        self.shipload = shipload

    #
    #   getRequests: Retorna las peticiones del lanzamiento
    #   @return ([str])
    #
    def getRequests(self) -> [str]:
        return self.requests

    #
    #   setRequests: Actualiza las peticiones del lanzamiento
    #   @param requests ([str]): Nuevos peticiones del lanzamiento
    #
    def setRequests(self, requests: [str]) -> None:
        self.requests = requests

    #
    #   getTime: Retorna tiempo del lanzamiento
    #   @return (Integer)
    #
    def getTime(self) -> int:
        return self.time

    #
    #   setTime: Actualiza el tiempo del lanzamiento
    #   @param time (Integer): Nuevo tiempo del lanzamiento
    #
    def setTime(self, time: int) -> None:
        self.time = time

    
    #
    #   getDispatched: Retorna el estado del lanzamiento
    #   @return (Boolean)
    #
    def getDispatched(self) -> bool:
        return self.dispatched

    #
    #   setDispatched: Actualiza el estado del lanzamiento
    #   @param dispatched (Boolean): Nuevo estado del lanzamiento
    #
    def setDispatched(self, dispatched: bool) -> None:
        self.dispatched = dispatched



    #
    #   getLaunchData: Devuelve un objeto con los datos del lanzamiento
    #   @return (dict)
    #
    def getLaunchData(self) -> dict:
        return {
            "id": self.id,
            "id_rocket": self.id_rocket,
            "max_weight": self.max_weight,
            "shipload": self.shipload,
            "requests": self.requests,
            "time": self.time,
            "dispatched": self.dispatched
        }
