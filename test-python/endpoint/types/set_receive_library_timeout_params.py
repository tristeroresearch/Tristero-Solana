from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetReceiveLibraryTimeoutParamsJSON(typing.TypedDict):
    receiver: str
    eid: int
    lib: str
    expiry: int


@dataclass
class SetReceiveLibraryTimeoutParams:
    layout: typing.ClassVar = borsh.CStruct(
        "receiver" / BorshPubkey,
        "eid" / borsh.U32,
        "lib" / BorshPubkey,
        "expiry" / borsh.U64,
    )
    receiver: Pubkey
    eid: int
    lib: Pubkey
    expiry: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetReceiveLibraryTimeoutParams":
        return cls(receiver=obj.receiver, eid=obj.eid, lib=obj.lib, expiry=obj.expiry)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "receiver": self.receiver,
            "eid": self.eid,
            "lib": self.lib,
            "expiry": self.expiry,
        }

    def to_json(self) -> SetReceiveLibraryTimeoutParamsJSON:
        return {
            "receiver": str(self.receiver),
            "eid": self.eid,
            "lib": str(self.lib),
            "expiry": self.expiry,
        }

    @classmethod
    def from_json(
        cls, obj: SetReceiveLibraryTimeoutParamsJSON
    ) -> "SetReceiveLibraryTimeoutParams":
        return cls(
            receiver=Pubkey.from_string(obj["receiver"]),
            eid=obj["eid"],
            lib=Pubkey.from_string(obj["lib"]),
            expiry=obj["expiry"],
        )
