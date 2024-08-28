from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class ConfirmMatchParamsJSON(typing.TypedDict):
    trade_match_id: int


@dataclass
class ConfirmMatchParams:
    layout: typing.ClassVar = borsh.CStruct("trade_match_id" / borsh.U64)
    trade_match_id: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "ConfirmMatchParams":
        return cls(trade_match_id=obj.trade_match_id)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"trade_match_id": self.trade_match_id}

    def to_json(self) -> ConfirmMatchParamsJSON:
        return {"trade_match_id": self.trade_match_id}

    @classmethod
    def from_json(cls, obj: ConfirmMatchParamsJSON) -> "ConfirmMatchParams":
        return cls(trade_match_id=obj["trade_match_id"])
