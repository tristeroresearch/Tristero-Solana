from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class InitDefaultSendLibraryParamsJSON(typing.TypedDict):
    eid: int
    new_lib: str


@dataclass
class InitDefaultSendLibraryParams:
    layout: typing.ClassVar = borsh.CStruct("eid" / borsh.U32, "new_lib" / BorshPubkey)
    eid: int
    new_lib: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitDefaultSendLibraryParams":
        return cls(eid=obj.eid, new_lib=obj.new_lib)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"eid": self.eid, "new_lib": self.new_lib}

    def to_json(self) -> InitDefaultSendLibraryParamsJSON:
        return {"eid": self.eid, "new_lib": str(self.new_lib)}

    @classmethod
    def from_json(
        cls, obj: InitDefaultSendLibraryParamsJSON
    ) -> "InitDefaultSendLibraryParams":
        return cls(eid=obj["eid"], new_lib=Pubkey.from_string(obj["new_lib"]))
