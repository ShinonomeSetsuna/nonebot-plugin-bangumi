from dataclasses import dataclass, is_dataclass, fields
from enum import Enum
from typing import NewType, Optional, get_args


class SortType(Enum):
    """排序方式枚举"""

    rank = "rank"
    score = "score"
    id = "id"


class SubjectType(Enum):
    """条目搜索枚举"""

    Book = 1
    Anime = 2
    Music = 3
    Game = 4
    Reality = 6  # 三次元该怎么表示……


@dataclass
class SubjectTag:
    """项目标签"""

    name: str
    """标签名"""
    count: int
    """标签数量"""


@dataclass
class Subject:
    """项目数据"""

    date: str
    """上映/发售日期"""
    image: str
    """图片链接"""
    type: SubjectType
    """项目类型"""
    summary: str
    """简介"""
    name: str
    """项目名"""
    name_cn: str
    """项目名称中文"""
    tags: list[SubjectTag]
    """标签"""
    score: float
    """评分"""
    id: int
    """项目id"""
    rank: int
    """项目排名"""


@dataclass
class ResponseMessage:
    """API返回数据"""

    data: list[Subject]
    """查询结果内容"""
    total: int
    """查询结果总数"""
    limit: int
    """单次返回内容限制"""
    offset: int
    """偏移量"""


AirDateRange = NewType("AirDateRange", str)
"""上映日期范围, str

(<|>|=)YYYY-MM-DD
"""
RatingRange = NewType("RatingRange", str)
"""评分范围, str

(<|>|=)Rating
"""
RankRange = NewType("RankRange", str)
"""排名范围, str

(<|>|=)Rank
"""

ErrorMessage = NewType("ErrorMessage", dict[str, str])


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
