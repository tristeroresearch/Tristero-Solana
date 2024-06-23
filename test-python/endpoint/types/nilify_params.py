from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class NilifyParamsJSON(typing.TypedDict):
    receiver: str
    src_eid: int
    sender: list[int]
    nonce: int
    payload_hash: list[int]


@dataclass
class NilifyParams:
    layout: typing.ClassVar = borsh.CStruct(
        "receiver" / BorshPubkey,
        "src_eid" / borsh.U32,
        "sender" / borsh.U8[32],
        "nonce" / borsh.U64,
        "payload_hash" / borsh.U8[32],
    )
    receiver: Pubkey
    src_eid: int
    sender: list[int]
    nonce: int
    payload_hash: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "NilifyParams":
        return cls(
            receiver=obj.receiver,
            src_eid=obj.src_eid,
            sender=obj.sender,
            nonce=obj.nonce,
            payload_hash=obj.payload_hash,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "receiver": self.receiver,
            "src_eid": self.src_eid,
            "sender": self.sender,
            "nonce": self.nonce,
            "payload_hash": self.payload_hash,
        }

    def to_json(self) -> NilifyParamsJSON:
        return {
            "receiver": str(self.receiver),
            "src_eid": self.src_eid,
            "sender": self.sender,
            "nonce": self.nonce,
            "payload_hash": self.payload_hash,
        }

    @classmethod
    def from_json(cls, obj: NilifyParamsJSON) -> "NilifyParams":
        return cls(
            receiver=Pubkey.from_string(obj["receiver"]),
            src_eid=obj["src_eid"],
            sender=obj["sender"],
            nonce=obj["nonce"],
            payload_hash=obj["payload_hash"],
        )
