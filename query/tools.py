from dataclasses import is_dataclass, fields
from typing import get_args


def from_dict(data_class: type, data: dict):
    """根据dict生成对应的dataclass实例

    Args:
        data_class (type): dataclass类
        data (dict): 数据

    Returns:
        DataClassInstance: 对应dataclass实例
    """
    if not is_dataclass(data_class):
        raise ValueError(f"{data_class} is not a dataclass")

    fieldtypes = {f.name: f.type for f in fields(data_class)}
    return data_class(
        **{
            f: from_dict(fieldtypes[f], data[f])
            if is_dataclass(fieldtypes[f])
            else (
                [from_dict(args, item) for item in data[f]]
                if is_dataclass(args := (get_args(fieldtypes[f]) or [None])[0])
                else data[f]
            )
            for f in data
        }
    )
