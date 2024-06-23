from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetSendLibraryParamsJSON(typing.TypedDict):
    sender: str
    eid: int
    new_lib: str


@dataclass
class SetSendLibraryParams:
    layout: typing.ClassVar = borsh.CStruct(
        "sender" / BorshPubkey, "eid" / borsh.U32, "new_lib" / BorshPubkey
    )
    sender: Pubkey
    eid: int
    new_lib: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetSendLibraryParams":
        return cls(sender=obj.sender, eid=obj.eid, new_lib=obj.new_lib)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"sender": self.sender, "eid": self.eid, "new_lib": self.new_lib}

    def to_json(self) -> SetSendLibraryParamsJSON:
        return {
            "sender": str(self.sender),
            "eid": self.eid,
            "new_lib": str(self.new_lib),
        }

    @classmethod
    def from_json(cls, obj: SetSendLibraryParamsJSON) -> "SetSendLibraryParams":
        return cls(
            sender=Pubkey.from_string(obj["sender"]),
            eid=obj["eid"],
            new_lib=Pubkey.from_string(obj["new_lib"]),
        )
