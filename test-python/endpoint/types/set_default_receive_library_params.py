from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetDefaultReceiveLibraryParamsJSON(typing.TypedDict):
    eid: int
    new_lib: str
    grace_period: int


@dataclass
class SetDefaultReceiveLibraryParams:
    layout: typing.ClassVar = borsh.CStruct(
        "eid" / borsh.U32, "new_lib" / BorshPubkey, "grace_period" / borsh.U64
    )
    eid: int
    new_lib: Pubkey
    grace_period: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetDefaultReceiveLibraryParams":
        return cls(eid=obj.eid, new_lib=obj.new_lib, grace_period=obj.grace_period)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "eid": self.eid,
            "new_lib": self.new_lib,
            "grace_period": self.grace_period,
        }

    def to_json(self) -> SetDefaultReceiveLibraryParamsJSON:
        return {
            "eid": self.eid,
            "new_lib": str(self.new_lib),
            "grace_period": self.grace_period,
        }

    @classmethod
    def from_json(
        cls, obj: SetDefaultReceiveLibraryParamsJSON
    ) -> "SetDefaultReceiveLibraryParams":
        return cls(
            eid=obj["eid"],
            new_lib=Pubkey.from_string(obj["new_lib"]),
            grace_period=obj["grace_period"],
        )
