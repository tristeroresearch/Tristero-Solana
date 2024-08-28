from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class ExecuteMatchParamsJSON(typing.TypedDict):
    dst_eid: int
    trade_match_id: int
    tristero_oapp_bump: int
    source_sell_amount: int
    receiver: list[int]


@dataclass
class ExecuteMatchParams:
    layout: typing.ClassVar = borsh.CStruct(
        "dst_eid" / borsh.U32,
        "trade_match_id" / borsh.U64,
        "tristero_oapp_bump" / borsh.U8,
        "source_sell_amount" / borsh.U64,
        "receiver" / borsh.U8[32],
    )
    dst_eid: int
    trade_match_id: int
    tristero_oapp_bump: int
    source_sell_amount: int
    receiver: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "ExecuteMatchParams":
        return cls(
            dst_eid=obj.dst_eid,
            trade_match_id=obj.trade_match_id,
            tristero_oapp_bump=obj.tristero_oapp_bump,
            source_sell_amount=obj.source_sell_amount,
            receiver=obj.receiver,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "dst_eid": self.dst_eid,
            "trade_match_id": self.trade_match_id,
            "tristero_oapp_bump": self.tristero_oapp_bump,
            "source_sell_amount": self.source_sell_amount,
            "receiver": self.receiver,
        }

    def to_json(self) -> ExecuteMatchParamsJSON:
        return {
            "dst_eid": self.dst_eid,
            "trade_match_id": self.trade_match_id,
            "tristero_oapp_bump": self.tristero_oapp_bump,
            "source_sell_amount": self.source_sell_amount,
            "receiver": self.receiver,
        }

    @classmethod
    def from_json(cls, obj: ExecuteMatchParamsJSON) -> "ExecuteMatchParams":
        return cls(
            dst_eid=obj["dst_eid"],
            trade_match_id=obj["trade_match_id"],
            tristero_oapp_bump=obj["tristero_oapp_bump"],
            source_sell_amount=obj["source_sell_amount"],
            receiver=obj["receiver"],
        )
