from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MessagingFeeJSON(typing.TypedDict):
    native_fee: int
    lz_token_fee: int


@dataclass
class MessagingFee:
    layout: typing.ClassVar = borsh.CStruct(
        "native_fee" / borsh.U64, "lz_token_fee" / borsh.U64
    )
    native_fee: int
    lz_token_fee: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "MessagingFee":
        return cls(native_fee=obj.native_fee, lz_token_fee=obj.lz_token_fee)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"native_fee": self.native_fee, "lz_token_fee": self.lz_token_fee}

    def to_json(self) -> MessagingFeeJSON:
        return {"native_fee": self.native_fee, "lz_token_fee": self.lz_token_fee}

    @classmethod
    def from_json(cls, obj: MessagingFeeJSON) -> "MessagingFee":
        return cls(native_fee=obj["native_fee"], lz_token_fee=obj["lz_token_fee"])
