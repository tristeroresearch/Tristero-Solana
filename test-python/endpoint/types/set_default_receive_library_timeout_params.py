from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetDefaultReceiveLibraryTimeoutParamsJSON(typing.TypedDict):
    eid: int
    lib: str
    expiry: int


@dataclass
class SetDefaultReceiveLibraryTimeoutParams:
    layout: typing.ClassVar = borsh.CStruct(
        "eid" / borsh.U32, "lib" / BorshPubkey, "expiry" / borsh.U64
    )
    eid: int
    lib: Pubkey
    expiry: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetDefaultReceiveLibraryTimeoutParams":
        return cls(eid=obj.eid, lib=obj.lib, expiry=obj.expiry)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"eid": self.eid, "lib": self.lib, "expiry": self.expiry}

    def to_json(self) -> SetDefaultReceiveLibraryTimeoutParamsJSON:
        return {"eid": self.eid, "lib": str(self.lib), "expiry": self.expiry}

    @classmethod
    def from_json(
        cls, obj: SetDefaultReceiveLibraryTimeoutParamsJSON
    ) -> "SetDefaultReceiveLibraryTimeoutParams":
        return cls(
            eid=obj["eid"], lib=Pubkey.from_string(obj["lib"]), expiry=obj["expiry"]
        )
