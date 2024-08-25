from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class PlaceOrderParamsJSON(typing.TypedDict):
    source_sell_amount: int
    min_sell_amount: int
    dest_token_mint: list[int]
    dest_buy_amount: int
    order_id: int
    eid: int


@dataclass
class PlaceOrderParams:
    layout: typing.ClassVar = borsh.CStruct(
        "source_sell_amount" / borsh.U64,
        "min_sell_amount" / borsh.U64,
        "dest_token_mint" / borsh.U8[20],
        "dest_buy_amount" / borsh.U64,
        "order_id" / borsh.U64,
        "eid" / borsh.U32,
    )
    source_sell_amount: int
    min_sell_amount: int
    dest_token_mint: list[int]
    dest_buy_amount: int
    order_id: int
    eid: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "PlaceOrderParams":
        return cls(
            source_sell_amount=obj.source_sell_amount,
            min_sell_amount=obj.min_sell_amount,
            dest_token_mint=obj.dest_token_mint,
            dest_buy_amount=obj.dest_buy_amount,
            order_id=obj.order_id,
            eid=obj.eid,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "source_sell_amount": self.source_sell_amount,
            "min_sell_amount": self.min_sell_amount,
            "dest_token_mint": self.dest_token_mint,
            "dest_buy_amount": self.dest_buy_amount,
            "order_id": self.order_id,
            "eid": self.eid,
        }

    def to_json(self) -> PlaceOrderParamsJSON:
        return {
            "source_sell_amount": self.source_sell_amount,
            "min_sell_amount": self.min_sell_amount,
            "dest_token_mint": self.dest_token_mint,
            "dest_buy_amount": self.dest_buy_amount,
            "order_id": self.order_id,
            "eid": self.eid,
        }

    @classmethod
    def from_json(cls, obj: PlaceOrderParamsJSON) -> "PlaceOrderParams":
        return cls(
            source_sell_amount=obj["source_sell_amount"],
            min_sell_amount=obj["min_sell_amount"],
            dest_token_mint=obj["dest_token_mint"],
            dest_buy_amount=obj["dest_buy_amount"],
            order_id=obj["order_id"],
            eid=obj["eid"],
        )
