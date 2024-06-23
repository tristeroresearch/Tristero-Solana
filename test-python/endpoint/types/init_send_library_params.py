from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class InitSendLibraryParamsJSON(typing.TypedDict):
    sender: str
    eid: int


@dataclass
class InitSendLibraryParams:
    layout: typing.ClassVar = borsh.CStruct("sender" / BorshPubkey, "eid" / borsh.U32)
    sender: Pubkey
    eid: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitSendLibraryParams":
        return cls(sender=obj.sender, eid=obj.eid)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"sender": self.sender, "eid": self.eid}

    def to_json(self) -> InitSendLibraryParamsJSON:
        return {"sender": str(self.sender), "eid": self.eid}

    @classmethod
    def from_json(cls, obj: InitSendLibraryParamsJSON) -> "InitSendLibraryParams":
        return cls(sender=Pubkey.from_string(obj["sender"]), eid=obj["eid"])
