from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class InitVerifyParamsJSON(typing.TypedDict):
    src_eid: int
    sender: list[int]
    receiver: str
    nonce: int


@dataclass
class InitVerifyParams:
    layout: typing.ClassVar = borsh.CStruct(
        "src_eid" / borsh.U32,
        "sender" / borsh.U8[32],
        "receiver" / BorshPubkey,
        "nonce" / borsh.U64,
    )
    src_eid: int
    sender: list[int]
    receiver: Pubkey
    nonce: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitVerifyParams":
        return cls(
            src_eid=obj.src_eid,
            sender=obj.sender,
            receiver=obj.receiver,
            nonce=obj.nonce,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "src_eid": self.src_eid,
            "sender": self.sender,
            "receiver": self.receiver,
            "nonce": self.nonce,
        }

    def to_json(self) -> InitVerifyParamsJSON:
        return {
            "src_eid": self.src_eid,
            "sender": self.sender,
            "receiver": str(self.receiver),
            "nonce": self.nonce,
        }

    @classmethod
    def from_json(cls, obj: InitVerifyParamsJSON) -> "InitVerifyParams":
        return cls(
            src_eid=obj["src_eid"],
            sender=obj["sender"],
            receiver=Pubkey.from_string(obj["receiver"]),
            nonce=obj["nonce"],
        )
