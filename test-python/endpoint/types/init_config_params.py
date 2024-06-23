from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class InitConfigParamsJSON(typing.TypedDict):
    oapp: str
    eid: int


@dataclass
class InitConfigParams:
    layout: typing.ClassVar = borsh.CStruct("oapp" / BorshPubkey, "eid" / borsh.U32)
    oapp: Pubkey
    eid: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitConfigParams":
        return cls(oapp=obj.oapp, eid=obj.eid)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"oapp": self.oapp, "eid": self.eid}

    def to_json(self) -> InitConfigParamsJSON:
        return {"oapp": str(self.oapp), "eid": self.eid}

    @classmethod
    def from_json(cls, obj: InitConfigParamsJSON) -> "InitConfigParams":
        return cls(oapp=Pubkey.from_string(obj["oapp"]), eid=obj["eid"])
