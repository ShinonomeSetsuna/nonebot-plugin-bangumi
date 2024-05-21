from enum import Enum
from typing import NewType


class SortType(Enum):
    """排序方式枚举"""

    Rank = "rank"
    Score = "score"
    Id = "id"


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
