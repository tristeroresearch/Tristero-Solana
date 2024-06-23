from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class SendParamsJSON(typing.TypedDict):
    dst_eid: int
    receiver: list[int]
    message: list[int]
    options: list[int]
    native_fee: int
    lz_token_fee: int


@dataclass
class SendParams:
    layout: typing.ClassVar = borsh.CStruct(
        "dst_eid" / borsh.U32,
        "receiver" / borsh.U8[32],
        "message" / borsh.Bytes,
        "options" / borsh.Bytes,
        "native_fee" / borsh.U64,
        "lz_token_fee" / borsh.U64,
    )
    dst_eid: int
    receiver: list[int]
    message: bytes
    options: bytes
    native_fee: int
    lz_token_fee: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SendParams":
        return cls(
            dst_eid=obj.dst_eid,
            receiver=obj.receiver,
            message=obj.message,
            options=obj.options,
            native_fee=obj.native_fee,
            lz_token_fee=obj.lz_token_fee,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "dst_eid": self.dst_eid,
            "receiver": self.receiver,
            "message": self.message,
            "options": self.options,
            "native_fee": self.native_fee,
            "lz_token_fee": self.lz_token_fee,
        }

    def to_json(self) -> SendParamsJSON:
        return {
            "dst_eid": self.dst_eid,
            "receiver": self.receiver,
            "message": list(self.message),
            "options": list(self.options),
            "native_fee": self.native_fee,
            "lz_token_fee": self.lz_token_fee,
        }

    @classmethod
    def from_json(cls, obj: SendParamsJSON) -> "SendParams":
        return cls(
            dst_eid=obj["dst_eid"],
            receiver=obj["receiver"],
            message=bytes(obj["message"]),
            options=bytes(obj["options"]),
            native_fee=obj["native_fee"],
            lz_token_fee=obj["lz_token_fee"],
        )
