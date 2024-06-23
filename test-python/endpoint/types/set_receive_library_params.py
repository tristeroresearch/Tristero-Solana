from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetReceiveLibraryParamsJSON(typing.TypedDict):
    receiver: str
    eid: int
    new_lib: str
    grace_period: int


@dataclass
class SetReceiveLibraryParams:
    layout: typing.ClassVar = borsh.CStruct(
        "receiver" / BorshPubkey,
        "eid" / borsh.U32,
        "new_lib" / BorshPubkey,
        "grace_period" / borsh.U64,
    )
    receiver: Pubkey
    eid: int
    new_lib: Pubkey
    grace_period: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetReceiveLibraryParams":
        return cls(
            receiver=obj.receiver,
            eid=obj.eid,
            new_lib=obj.new_lib,
            grace_period=obj.grace_period,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "receiver": self.receiver,
            "eid": self.eid,
            "new_lib": self.new_lib,
            "grace_period": self.grace_period,
        }

    def to_json(self) -> SetReceiveLibraryParamsJSON:
        return {
            "receiver": str(self.receiver),
            "eid": self.eid,
            "new_lib": str(self.new_lib),
            "grace_period": self.grace_period,
        }

    @classmethod
    def from_json(cls, obj: SetReceiveLibraryParamsJSON) -> "SetReceiveLibraryParams":
        return cls(
            receiver=Pubkey.from_string(obj["receiver"]),
            eid=obj["eid"],
            new_lib=Pubkey.from_string(obj["new_lib"]),
            grace_period=obj["grace_period"],
        )
