from __future__ import annotations
from . import (
    messaging_fee,
)
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MessagingReceiptJSON(typing.TypedDict):
    guid: list[int]
    nonce: int
    fee: messaging_fee.MessagingFeeJSON


@dataclass
class MessagingReceipt:
    layout: typing.ClassVar = borsh.CStruct(
        "guid" / borsh.U8[32],
        "nonce" / borsh.U64,
        "fee" / messaging_fee.MessagingFee.layout,
    )
    guid: list[int]
    nonce: int
    fee: messaging_fee.MessagingFee

    @classmethod
    def from_decoded(cls, obj: Container) -> "MessagingReceipt":
        return cls(
            guid=obj.guid,
            nonce=obj.nonce,
            fee=messaging_fee.MessagingFee.from_decoded(obj.fee),
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"guid": self.guid, "nonce": self.nonce, "fee": self.fee.to_encodable()}

    def to_json(self) -> MessagingReceiptJSON:
        return {"guid": self.guid, "nonce": self.nonce, "fee": self.fee.to_json()}

    @classmethod
    def from_json(cls, obj: MessagingReceiptJSON) -> "MessagingReceipt":
        return cls(
            guid=obj["guid"],
            nonce=obj["nonce"],
            fee=messaging_fee.MessagingFee.from_json(obj["fee"]),
        )
