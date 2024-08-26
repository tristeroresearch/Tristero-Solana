from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class CreateMatchParamsJSON(typing.TypedDict):
    src_index: int
    dst_index: int
    src_quantity: int
    dst_quantity: int
    trade_match_id: int


@dataclass
class CreateMatchParams:
    layout: typing.ClassVar = borsh.CStruct(
        "src_index" / borsh.U64,
        "dst_index" / borsh.U64,
        "src_quantity" / borsh.U64,
        "dst_quantity" / borsh.U64,
        "trade_match_id" / borsh.U64,
    )
    src_index: int
    dst_index: int
    src_quantity: int
    dst_quantity: int
    trade_match_id: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "CreateMatchParams":
        return cls(
            src_index=obj.src_index,
            dst_index=obj.dst_index,
            src_quantity=obj.src_quantity,
            dst_quantity=obj.dst_quantity,
            trade_match_id=obj.trade_match_id,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "src_index": self.src_index,
            "dst_index": self.dst_index,
            "src_quantity": self.src_quantity,
            "dst_quantity": self.dst_quantity,
            "trade_match_id": self.trade_match_id,
        }

    def to_json(self) -> CreateMatchParamsJSON:
        return {
            "src_index": self.src_index,
            "dst_index": self.dst_index,
            "src_quantity": self.src_quantity,
            "dst_quantity": self.dst_quantity,
            "trade_match_id": self.trade_match_id,
        }

    @classmethod
    def from_json(cls, obj: CreateMatchParamsJSON) -> "CreateMatchParams":
        return cls(
            src_index=obj["src_index"],
            dst_index=obj["dst_index"],
            src_quantity=obj["src_quantity"],
            dst_quantity=obj["dst_quantity"],
            trade_match_id=obj["trade_match_id"],
        )
