from enum import Enum
import json
from typing import Optional, overload
import requests
from .tokens import BANGUMI_TOKEN
from ..api_tpyes.subject_types import (
    ErrorMessage,
    SortType,
    SubjectType,
    AirDateRange,
    RankRange,
    RatingRange,
    ResponseMessage,
    from_dict,
)

BASE = "https://api.bgm.tv"


def strict_mode(
    data: dict, ignore_score: bool = False, ignore_rank: bool = False
) -> bool:
    """限制模式，排除不具有分数和排名的内容

    Args:
        data (dict): 项目数据
        ignore_score (bool, optional): 加入没有评分的项目. 默认为否.
        ignore_rank (bool, optional): 加入没有排名的项目. 默认为否.

    Returns:
        bool: 是否保留该项目
    """
    return (data["score"] or ignore_score) and (data["rank"] or ignore_rank)


@overload
def subjects_search(
    keyword: str,
    sort: SortType,
    type: Optional[list[SubjectType]] = None,
    tag: Optional[list[str]] = None,
    air_date: Optional[list[AirDateRange]] = None,
    rating: Optional[list[RatingRange]] = None,
    rank: Optional[list[RankRange]] = None,
    nsfw: bool = False,
) -> ResponseMessage | ErrorMessage:
    """在Bangumi中使用`keyword`搜索

    Args:
        keyword (str): 关键字，要搜索的内容
        sort (SortType): 排序方式
        type (Optional[list[SubjectType]]): 内容分类. 可为空
        tag (Optional[list[str]]): 标签. 可为空
        airdate (Optional[list[AirDateRange]]): 发售日期. 可为空
        rating (Optional[list[RatingRange]]): 排名. 可为空
        rank (Optional[list[RankRange]]): 排名. 可为空
        nsfw (bool): 工作场所不宜.

    Returns:
        dict[str, str]: API返回结果
    """
    pass


def subjects_search(
    keyword: str, sort: SortType, **kwargs: dict
) -> ResponseMessage | ErrorMessage:
    data = {
        "keyword": keyword,
        "sort": sort.value,
        "filter": {
            k: (
                [sub.value if isinstance(sub, Enum) else sub for sub in v]
                if isinstance(v, list)
                else ([v.value] if isinstance(v, Enum) else [v])
            )
            for k, v in kwargs.items()
        },
    }
    print(data)
    r = requests.post(
        url=BASE + "/v0/search/subjects",
        headers={
            "Authorization": f"Bearer {BANGUMI_TOKEN}",
            "accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "ShinonomeSetsuna/nonebot-plugin-bangumi (https://github.com/ShinonomeSetsuna/nonebot-plugin-bangumi)",
        },
        data=json.dumps(data),
    )
    try:
        return from_dict(
            ResponseMessage,
            {
                k: v if k != "data" else [data for data in v if strict_mode(data)]
                for k, v in r.json().items()
            },
        )
    except Exception:
        return r.json()


if __name__ == "__main__":
    print(str(SubjectType.Book.value))
    print(type(SubjectType.Anime.value))
    res = subjects_search(
        "Eden*",
        SortType.score,
        type=SubjectType.Game,
        # rating=["=7.3"],
        # rank=[""],
    )
    print("aaa")
