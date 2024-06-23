from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class ClearComposeParamsJSON(typing.TypedDict):
    from_: str
    guid: list[int]
    index: int
    message: list[int]


@dataclass
class ClearComposeParams:
    layout: typing.ClassVar = borsh.CStruct(
        "from_" / BorshPubkey,
        "guid" / borsh.U8[32],
        "index" / borsh.U16,
        "message" / borsh.Bytes,
    )
    from_: Pubkey
    guid: list[int]
    index: int
    message: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "ClearComposeParams":
        return cls(from_=obj.from_, guid=obj.guid, index=obj.index, message=obj.message)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "from_": self.from_,
            "guid": self.guid,
            "index": self.index,
            "message": self.message,
        }

    def to_json(self) -> ClearComposeParamsJSON:
        return {
            "from_": str(self.from_),
            "guid": self.guid,
            "index": self.index,
            "message": list(self.message),
        }

    @classmethod
    def from_json(cls, obj: ClearComposeParamsJSON) -> "ClearComposeParams":
        return cls(
            from_=Pubkey.from_string(obj["from"]),
            guid=obj["guid"],
            index=obj["index"],
            message=bytes(obj["message"]),
        )
