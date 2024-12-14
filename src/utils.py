import re
from src.evaluetype import EValueType

def validate_db_fields(name: str, pattern: str = r'^[a-z0-9_]+$'):
    if not re.match(pattern, name):
        raise Exception("An invalid character has been entered, available set [a-z0-9_]")


def validate_row_data(name: str, pattern: str = r'^[a-zA-Z0-9_!?,.@#%^&*()\-=+~]+$'):
    if not re.match(pattern, name):
        raise Exception("An invalid character has been entered, available set [a-z0-9_]")


def convert_to_e_value_type(value) -> EValueType:
    from src.entities.link import Link

    if type(value) == int:
        return EValueType.INT
    elif type(value) == float:
        return EValueType.FLOAT
    elif type(value) == str:
        return EValueType.STRING
    elif type(value) == Link:
        return EValueType.LINK
    else:
        return EValueType.UNKNOWN