from src import Column


class Table:
    __name: str
    __columns: list[Column]

    def __init__(self, name: str, cols: list[Column]):
        self.__name = name
        self.__columns = cols

    @property
    def name(self): return self.__name

    @property
    def columns(self): return self.__columns
