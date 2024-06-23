from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class InitReceiveLibraryParamsJSON(typing.TypedDict):
    receiver: str
    eid: int


@dataclass
class InitReceiveLibraryParams:
    layout: typing.ClassVar = borsh.CStruct("receiver" / BorshPubkey, "eid" / borsh.U32)
    receiver: Pubkey
    eid: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitReceiveLibraryParams":
        return cls(receiver=obj.receiver, eid=obj.eid)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"receiver": self.receiver, "eid": self.eid}

    def to_json(self) -> InitReceiveLibraryParamsJSON:
        return {"receiver": str(self.receiver), "eid": self.eid}

    @classmethod
    def from_json(cls, obj: InitReceiveLibraryParamsJSON) -> "InitReceiveLibraryParams":
        return cls(receiver=Pubkey.from_string(obj["receiver"]), eid=obj["eid"])
