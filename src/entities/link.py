from src.utils import validate_db_fields

class Link:
    __table_name: str
    __row_index: int

    def __init__(self, table_name: str, row_index: int):
        validate_db_fields(table_name)

        self.__table_name = table_name
        self.__row_index = row_index

    @property
    def table_name(self) -> str:
        return self.__table_name

    @property
    def row_index(self) -> int:
        return self.__row_index

    def __repr__(self):
        return "Link"