from src import EValueType


class Column:
    __name: str
    __type: EValueType

    def __init__(self, name: str, col_type: EValueType):
        self.__name = name
        self.__type = col_type

    @property
    def name(self) -> str: return self.__name

    @property
    def type(self) -> str: return self.__type.value
