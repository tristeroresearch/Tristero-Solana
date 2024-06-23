from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SendComposeParamsJSON(typing.TypedDict):
    to: str
    guid: list[int]
    index: int
    message: list[int]


@dataclass
class SendComposeParams:
    layout: typing.ClassVar = borsh.CStruct(
        "to" / BorshPubkey,
        "guid" / borsh.U8[32],
        "index" / borsh.U16,
        "message" / borsh.Bytes,
    )
    to: Pubkey
    guid: list[int]
    index: int
    message: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "SendComposeParams":
        return cls(to=obj.to, guid=obj.guid, index=obj.index, message=obj.message)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "to": self.to,
            "guid": self.guid,
            "index": self.index,
            "message": self.message,
        }

    def to_json(self) -> SendComposeParamsJSON:
        return {
            "to": str(self.to),
            "guid": self.guid,
            "index": self.index,
            "message": list(self.message),
        }

    @classmethod
    def from_json(cls, obj: SendComposeParamsJSON) -> "SendComposeParams":
        return cls(
            to=Pubkey.from_string(obj["to"]),
            guid=obj["guid"],
            index=obj["index"],
            message=bytes(obj["message"]),
        )
