from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class RegisterOAppParamsJSON(typing.TypedDict):
    delegate: str


@dataclass
class RegisterOAppParams:
    layout: typing.ClassVar = borsh.CStruct("delegate" / BorshPubkey)
    delegate: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "RegisterOAppParams":
        return cls(delegate=obj.delegate)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"delegate": self.delegate}

    def to_json(self) -> RegisterOAppParamsJSON:
        return {"delegate": str(self.delegate)}

    @classmethod
    def from_json(cls, obj: RegisterOAppParamsJSON) -> "RegisterOAppParams":
        return cls(delegate=Pubkey.from_string(obj["delegate"]))
