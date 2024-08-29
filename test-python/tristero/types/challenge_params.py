from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class ChallengeParamsJSON(typing.TypedDict):
    trade_match_id: int
    tristero_oapp_bump: int
    receiver: list[int]
    taker: list[int]


@dataclass
class ChallengeParams:
    layout: typing.ClassVar = borsh.CStruct(
        "trade_match_id" / borsh.U64,
        "tristero_oapp_bump" / borsh.U8,
        "receiver" / borsh.U8[32],
        "taker" / borsh.U8[20],
    )
    trade_match_id: int
    tristero_oapp_bump: int
    receiver: list[int]
    taker: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "ChallengeParams":
        return cls(
            trade_match_id=obj.trade_match_id,
            tristero_oapp_bump=obj.tristero_oapp_bump,
            receiver=obj.receiver,
            taker=obj.taker,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "trade_match_id": self.trade_match_id,
            "tristero_oapp_bump": self.tristero_oapp_bump,
            "receiver": self.receiver,
            "taker": self.taker,
        }

    def to_json(self) -> ChallengeParamsJSON:
        return {
            "trade_match_id": self.trade_match_id,
            "tristero_oapp_bump": self.tristero_oapp_bump,
            "receiver": self.receiver,
            "taker": self.taker,
        }

    @classmethod
    def from_json(cls, obj: ChallengeParamsJSON) -> "ChallengeParams":
        return cls(
            trade_match_id=obj["trade_match_id"],
            tristero_oapp_bump=obj["tristero_oapp_bump"],
            receiver=obj["receiver"],
            taker=obj["taker"],
        )
