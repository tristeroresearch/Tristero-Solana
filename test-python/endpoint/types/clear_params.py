from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class ClearParamsJSON(typing.TypedDict):
    receiver: str
    src_eid: int
    sender: list[int]
    nonce: int
    guid: list[int]
    message: list[int]


@dataclass
class ClearParams:
    layout: typing.ClassVar = borsh.CStruct(
        "receiver" / BorshPubkey,
        "src_eid" / borsh.U32,
        "sender" / borsh.U8[32],
        "nonce" / borsh.U64,
        "guid" / borsh.U8[32],
        "message" / borsh.Bytes,
    )
    receiver: Pubkey
    src_eid: int
    sender: list[int]
    nonce: int
    guid: list[int]
    message: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "ClearParams":
        return cls(
            receiver=obj.receiver,
            src_eid=obj.src_eid,
            sender=obj.sender,
            nonce=obj.nonce,
            guid=obj.guid,
            message=obj.message,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "receiver": self.receiver,
            "src_eid": self.src_eid,
            "sender": self.sender,
            "nonce": self.nonce,
            "guid": self.guid,
            "message": self.message,
        }

    def to_json(self) -> ClearParamsJSON:
        return {
            "receiver": str(self.receiver),
            "src_eid": self.src_eid,
            "sender": self.sender,
            "nonce": self.nonce,
            "guid": self.guid,
            "message": list(self.message),
        }

    @classmethod
    def from_json(cls, obj: ClearParamsJSON) -> "ClearParams":
        return cls(
            receiver=Pubkey.from_string(obj["receiver"]),
            src_eid=obj["src_eid"],
            sender=obj["sender"],
            nonce=obj["nonce"],
            guid=obj["guid"],
            message=bytes(obj["message"]),
        )
