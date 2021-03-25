from processes import translate

class Rocket:

    #
    #   __init__: Inicializa la clase
    #   @param name (String): Identificador del cohete
    #   @param shipload (Integer): Carga máxima del cohete
    #
    def __init__(self, name: str, shipload: int) -> None:
        self.id = name
        self.shipload = shipload

    #
    #   __str__: Retorna los datos del cohete para imprimirlos por pantalla
    #   @return (String)
    #
    def __str__(self) -> str:
        return "\n# " + translate.getValue('COMMON.NAME') + ": " + self.id + "\n  " + translate.getValue('COMMON.OTB') + ": " + str(self.shipload/1000) + " kg." 
    
    #
    #   getId: Retorna el identificador del cohete
    #   @return (String)
    #
    def getId(self) -> str:
        return self.id

    #
    #   setId: Actualiza el identificador del cohete
    #   @param name (String): Nuevo identificador para el cohete
    #
    def setId(self, name: str) -> None:
        self.id = name

    #
    #   getShipload: Retorna la carga máxima del cohete
    #   @return (Integer)
    #
    def getShipload(self) -> int:
        return self.shipload

    #
    #   setShipload: Actualiza la carga máxima del cohete
    #   @param shipload (Integer): Nueva carga máxima para el cohete
    #
    def setShipload(self, shipload: int) -> None:
        self.shipload = shipload

    #
    #   getRocketData: Devuelve un objeto con los datos del cohete
    #   @return (dict)
    #
    def getRocketData(self) -> dict:
        return {
            "id": self.getId(),
            "shipload": self.getShipload()
        }
