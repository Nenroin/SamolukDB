from src.utils import validate_db_fields


class Link:
    __table_name: str
    __row_id: int
    __col_name: str

    def __init__(self, table_name: str, row_id: int, col_name: str):
        validate_db_fields(table_name)

        self.__col_name = col_name
        self.__table_name = table_name
        self.__row_id = row_id

    @property
    def table_name(self) -> str:
        return self.__table_name

    @property
    def row_id(self) -> int:
        return self.__row_id

    @property
    def col_name(self) -> str:
        return self.__col_name

    def __str__(self):
        return f"{self.table_name}, {self.row_id}, {self.col_name}"

    def __repr__(self):
        return f"Link({self.table_name}, {self.row_id}, {self.col_name})"
