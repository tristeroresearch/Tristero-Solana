from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class TransferAdminParamsJSON(typing.TypedDict):
    admin: str


@dataclass
class TransferAdminParams:
    layout: typing.ClassVar = borsh.CStruct("admin" / BorshPubkey)
    admin: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "TransferAdminParams":
        return cls(admin=obj.admin)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"admin": self.admin}

    def to_json(self) -> TransferAdminParamsJSON:
        return {"admin": str(self.admin)}

    @classmethod
    def from_json(cls, obj: TransferAdminParamsJSON) -> "TransferAdminParams":
        return cls(admin=Pubkey.from_string(obj["admin"]))
