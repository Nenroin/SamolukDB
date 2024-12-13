class DBManager:
    path_to_db: str
    __db_name: str

    def __init__(self, path_to_db):
        pass

    def delete_table(self):
        pass

    def get_list(self, table_name: str):
        pass

    def get_item(self, table_name: str, item_id: str):
        pass

    def add_item(self, table_name: str, data: dict):
        pass

    def update_item(self, table_name: str, item_id: str, data: dict):
        pass

    def delete_item(self, table_name: str, item_id: str):
        pass
