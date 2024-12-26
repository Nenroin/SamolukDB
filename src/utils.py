import re
from src.evaluetype import EValueType


def validate_db_fields(name: str, pattern: str = r'^[a-z0-9_]+$'):
    if not re.match(pattern, name):
        raise Exception("An invalid character has been entered, available set [a-z0-9_]")


def validate_row_data(name: str, pattern: str = r'^[a-zA-Zа-яА-ЯёЁ0-9_ :!?,.@#%^&*()\/\-+=\~]+$'):
    if not re.match(pattern, name):
        raise Exception("An invalid character has been entered, available set [a-zA-Zа-яА-Я0-9_!?,.@#%\^&*()\/\-+=\~]")


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


def convert_to(value: str, eval_type: EValueType) -> any:
    from src.entities.link import Link

    match eval_type:
        case EValueType.INT:
            return int(value)
        case EValueType.FLOAT:
            return float(value)
        case EValueType.STRING:
            return str(value)
        case EValueType.LINK:
            split_value: list[str] = value.split(',')
            return Link(str(split_value[0]), int(split_value[1]), str(split_value[2]))
        case _:
            raise Exception("Unknown value type")
