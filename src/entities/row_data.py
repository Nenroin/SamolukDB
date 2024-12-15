from src import validate_row_data, convert_to_e_value_type
from src import EValueType
from src.entities.link import Link

class RowData:
    __data: list
    __links: list[Link]

    def __init__(self, data: list):
        self.__data = []
        self.__links = []

        for i in data:
            if convert_to_e_value_type(i) != EValueType.LINK:
                validate_row_data(str(i))
            elif convert_to_e_value_type(i) == EValueType.LINK:
                self.__links.append(i)
            self.__data.append(i)

    def check_types(self, types: list[str]):
        for idx, t in enumerate(types):
            if t != convert_to_e_value_type(self.__data[idx]).value:
                raise Exception("Invalid data type")

    def get_links(self) -> list[Link]:
        return self.__links.copy()

    def __getitem__(self, index):
        return self.__data[index]

    def __str__(self):
        return str(self.__data)

    def __iter__(self):
        return iter(self.__data.copy())

    def __len__(self):
        return len(self.__data)
