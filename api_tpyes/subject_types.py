from dataclasses import dataclass
from enum import Enum
from typing import NewType


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


ErrorMessage = NewType("ErrorMessage", dict[str, str])
