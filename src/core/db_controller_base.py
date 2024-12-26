from abc import ABC, abstractmethod
from src.entities.row_data import RowData
from src.entities.table import Table
from src.entities.link import Link


class DBControllerBase(ABC):
    @abstractmethod
    def late_init(self):
        pass

    @property
    @abstractmethod
    def db_name(self) -> str:
        pass

    @abstractmethod
    def add_tables(self, tables: list[Table]):
        pass

    @abstractmethod
    def delete_table(self, table_name: str):
        pass

    @abstractmethod
    def get_table_names(self) -> list[str]:
        pass

    @abstractmethod
    def get_table_row_names(self, table_name: str) -> list[str]:
        pass

    @abstractmethod
    def get_table_row_types(self, table_name: str) -> list[str]:
        pass

    @abstractmethod
    def add_item(self, table_name: str, data: RowData):
        pass

    @abstractmethod
    def update_item(self, table_name: str, item_id: int, data: RowData):
        pass

    @abstractmethod
    def delete_item(self, table_name: str, item_id: int):
        pass

    @abstractmethod
    def find_item_by_col_name(self, table_nane: str, col_name: str, col_value: any) -> any:
        pass

    @abstractmethod
    def find_item_by_col_idx(self, table_nane: str, col_index: int, col_value: any) -> any:
        pass

    @abstractmethod
    def get_item_by_link(self, link: Link) -> any:
        pass

    @abstractmethod
    def show_item_list(self, table_name: str):
        pass

    @abstractmethod
    def get_item_list(self, table_name: str) -> list[RowData]:
        pass

    @abstractmethod
    def get_item(self, table_name: str, item_id: int) -> RowData:
        pass

    @abstractmethod
    def delete_db(self):
        pass