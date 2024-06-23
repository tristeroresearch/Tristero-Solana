from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class UpdateUserParamsJSON(typing.TypedDict):
    new_user: str


@dataclass
class UpdateUserParams:
    layout: typing.ClassVar = borsh.CStruct("new_user" / BorshPubkey)
    new_user: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateUserParams":
        return cls(new_user=obj.new_user)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"new_user": self.new_user}

    def to_json(self) -> UpdateUserParamsJSON:
        return {"new_user": str(self.new_user)}

    @classmethod
    def from_json(cls, obj: UpdateUserParamsJSON) -> "UpdateUserParams":
        return cls(new_user=Pubkey.from_string(obj["new_user"]))
