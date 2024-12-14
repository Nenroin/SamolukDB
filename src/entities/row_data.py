from src import validate_row_data, convert_to_e_value_type
from src import EValueType


class RowData:
    __data: list

    def __init__(self, data: list):
        self.__data = []

        for i in data:
            if convert_to_e_value_type(i) != EValueType.LINK:
                validate_row_data(str(i))
            self.__data.append(i)

    def check_types(self, types: list[str]):
        for idx, t in enumerate(types):
            if t != convert_to_e_value_type(self.__data[idx]).value:
                raise Exception("Invalid data type")

    def __str__(self):
        return str(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __len__(self):
        return len(self.__data)