from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class QuoteParamsJSON(typing.TypedDict):
    sender: str
    dst_eid: int
    receiver: list[int]
    message: list[int]
    options: list[int]
    pay_in_lz_token: bool


@dataclass
class QuoteParams:
    layout: typing.ClassVar = borsh.CStruct(
        "sender" / BorshPubkey,
        "dst_eid" / borsh.U32,
        "receiver" / borsh.U8[32],
        "message" / borsh.Bytes,
        "options" / borsh.Bytes,
        "pay_in_lz_token" / borsh.Bool,
    )
    sender: Pubkey
    dst_eid: int
    receiver: list[int]
    message: bytes
    options: bytes
    pay_in_lz_token: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "QuoteParams":
        return cls(
            sender=obj.sender,
            dst_eid=obj.dst_eid,
            receiver=obj.receiver,
            message=obj.message,
            options=obj.options,
            pay_in_lz_token=obj.pay_in_lz_token,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "sender": self.sender,
            "dst_eid": self.dst_eid,
            "receiver": self.receiver,
            "message": self.message,
            "options": self.options,
            "pay_in_lz_token": self.pay_in_lz_token,
        }

    def to_json(self) -> QuoteParamsJSON:
        return {
            "sender": str(self.sender),
            "dst_eid": self.dst_eid,
            "receiver": self.receiver,
            "message": list(self.message),
            "options": list(self.options),
            "pay_in_lz_token": self.pay_in_lz_token,
        }

    @classmethod
    def from_json(cls, obj: QuoteParamsJSON) -> "QuoteParams":
        return cls(
            sender=Pubkey.from_string(obj["sender"]),
            dst_eid=obj["dst_eid"],
            receiver=obj["receiver"],
            message=bytes(obj["message"]),
            options=bytes(obj["options"]),
            pay_in_lz_token=obj["pay_in_lz_token"],
        )
