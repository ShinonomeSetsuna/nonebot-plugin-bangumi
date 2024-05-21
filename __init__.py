from nonebot import on_command
from nonebot.adapters.satori import MessageSegment, Message, event
from nonebot.params import CommandArg

from .query import subjects_query
from .api_tpyes import SortType, SubjectType


bangumi = on_command(("bangumi"))


@bangumi.handle()
async def _(e: event.Event, args: Message = CommandArg()):
    print(e.message.id)
    print(MessageSegment.at(e.get_user_id()))
    res = subjects_query("Eden*", sort=SortType.Rank, type=SubjectType.Game).data[0]
    print(res, type(res))
    await bangumi.send(Message([res.name, res.name_cn]))
