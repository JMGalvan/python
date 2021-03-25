from processes import translate

class Request:

    #
    #   __init__: Inicializa la clase
    #   @param name (String): Identificador de la petición
    #   @param weight (Integer): Peso de la petición
    #   @param description (String): Descripción de la petición
    #   @param time_max (Integer): Tiempo máximo de la petición
    #   @param dispatched (Boolean): Estado de la petición
    #
    def __init__(self, name: str, weight: int, description: str, time_max: int, dispatched: bool) -> None:
        self.id = name
        self.weight = weight
        self.description = description
        self.time_max = time_max
        self.dispatched = dispatched

    #
    #   __str__: Retorna los datos de la petición para imprimirlos por pantalla
    #   @return (String)
    #
    def __str__(self) -> str:
        status = ""
        if (self.time_max > 0):
            status = translate.getValue('COMMON.IN_TRANSIT') if self.dispatched else translate.getValue('COMMON.UNASSIGNED')
        else:
            status = translate.getValue('COMMON.DELIVERED') if self.dispatched else translate.getValue('COMMON.CANCELED')

        line0 = "\n# " + translate.getValue('COMMON.NAME') + ": " + self.id
        line1 = "\n  " + translate.getValue('COMMON.WEIGHT') + ": " + str(int(self.weight)/1000) + " kg." 
        line2 = "\n  " + translate.getValue('COMMON.MAX_DAYS') + ": " +  str(self.time_max) 
        line3 = "\n  " + translate.getValue('COMMON.DESCRIPTION') + ": " + self.description
        line4 = "\n  " + translate.getValue('COMMON.STATUS') + ": " + status
        return line0 + line1 + line2 + line3 + line4
    
    #
    #   getId: Retorna el identificador de la petición
    #   @return (String)
    #
    def getId(self) -> str:
        return self.id

    #
    #   setId: Actualiza el identificador de la petición
    #   @param name (String): Nuevo identificador para la petición
    #
    def setId(self, name: str) -> None:
        self.id = name

    #
    #   getWeight: Retorna peso de la petición
    #   @return (Integer)
    #
    def getWeight(self) -> int:
        return self.weight

    #
    #   setWeight: Actualiza el peso de la petición
    #   @param weight (Integer): Nueva peso de la petición
    #
    def setWeight(self, weight: int) -> None:
        self.weight = weight

    #
    #   getDescription: Retorna la descripción de la petición
    #   @return (String)
    #
    def getDescription(self) -> str:
        return self.description

    #
    #   setDescription: Actualiza la descripción de la petición
    #   @param description (String): Nueva descripción de la petición
    #
    def setDescription(self, description: str) -> None:
        self.description = description

    #
    #   getTimeMax: Retorna tiempo máximo de la petición
    #   @return (Integer)
    #
    def getTimeMax(self) -> int:
        return self.time_max

    #
    #   setTimeMax: Actualiza el tiempo máximo de la petición
    #   @param time_max (Integer): Nuevo tiempo máximo de la petición
    #
    def setTimeMax(self, time_max: int) -> None:
        self.time_max = time_max

    #
    #   getDispatched: Retorna el estado de la petición
    #   @return (Boolean)
    #
    def getDispatched(self) -> bool:
        return self.dispatched

    #
    #   setDispatched: Actualiza el estado de la petición
    #   @param dispatched (Boolean): Nuevo estado de la petición
    #
    def setDispatched(self, dispatched: bool) -> None:
        self.dispatched = dispatched


    #
    #   getRequestData: Devuelve un objeto con los datos de la petición
    #   @return (dict)
    #
    def getRequestData(self) -> dict:
        return {
            "id": self.id,
            "weight": self.weight,
            "description": self.description,
            "time_max": self.time_max,
            "dispatched": self.dispatched
        }
