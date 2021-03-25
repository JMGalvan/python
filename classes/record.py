from processes import translate

class Record:

    #
    #   __init__: Inicializa la clase
    #   @param name (String): Identificador del registro
    #   @param value (Integer): Valor del registro
    #
    def __init__(self, name: str, value: str) -> None:
        self.id = name
        self.value = value

    #
    #   __str__: Retorna los datos del registro para imprimirlos por pantalla
    #   @return (String)
    #
    def __str__(self) -> str:
        return "\n# " + translate.getValue(self.id) + ": " + self.value
    
    #
    #   getId: Retorna el identificador del registro
    #   @return (String)
    #
    def getId(self) -> str:
        return self.id

    #
    #   setId: Actualiza el identificador del registro
    #   @param name (String): Nuevo identificador para el registro
    #
    def setId(self, name: str) -> None:
        self.id = name

    #
    #   getValue: Retorna el valor del registro
    #   @return (Integer)
    #
    def getValue(self) -> str:
        return self.value

    #
    #   setValue: Actualiza el valor del registro
    #   @param value (Integer): Nuevo valor para el registro
    #
    def setValue(self, value: str) -> None:
        self.value = value

    #
    #   getRecordData: Devuelve un objeto con los datos del registro
    #   @return (dict)
    #
    def getRecordData(self) -> dict:
        return {
            "id": self.getId(),
            "value": self.getValue()
        }
