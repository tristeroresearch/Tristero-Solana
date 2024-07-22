from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class LzReceiveParamsJSON(typing.TypedDict):
    src_eid: int
    sender: list[int]
    nonce: int
    guid: list[int]
    message: list[int]
    extra_data: list[int]


@dataclass
class LzReceiveParams:
    layout: typing.ClassVar = borsh.CStruct(
        "src_eid" / borsh.U32,
        "sender" / borsh.U8[32],
        "nonce" / borsh.U64,
        "guid" / borsh.U8[32],
        "message" / borsh.Bytes,
        "extra_data" / borsh.Bytes,
    )
    src_eid: int
    sender: list[int]
    nonce: int
    guid: list[int]
    message: bytes
    extra_data: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "LzReceiveParams":
        return cls(
            src_eid=obj.src_eid,
            sender=obj.sender,
            nonce=obj.nonce,
            guid=obj.guid,
            message=obj.message,
            extra_data=obj.extra_data,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "src_eid": self.src_eid,
            "sender": self.sender,
            "nonce": self.nonce,
            "guid": self.guid,
            "message": self.message,
            "extra_data": self.extra_data,
        }

    def to_json(self) -> LzReceiveParamsJSON:
        return {
            "src_eid": self.src_eid,
            "sender": self.sender,
            "nonce": self.nonce,
            "guid": self.guid,
            "message": list(self.message),
            "extra_data": list(self.extra_data),
        }

    @classmethod
    def from_json(cls, obj: LzReceiveParamsJSON) -> "LzReceiveParams":
        return cls(
            src_eid=obj["src_eid"],
            sender=obj["sender"],
            nonce=obj["nonce"],
            guid=obj["guid"],
            message=bytes(obj["message"]),
            extra_data=bytes(obj["extra_data"]),
        )
