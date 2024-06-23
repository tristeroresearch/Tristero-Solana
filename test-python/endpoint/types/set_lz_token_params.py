from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetLzTokenParamsJSON(typing.TypedDict):
    lz_token: typing.Optional[str]


@dataclass
class SetLzTokenParams:
    layout: typing.ClassVar = borsh.CStruct("lz_token" / borsh.Option(BorshPubkey))
    lz_token: typing.Optional[Pubkey]

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetLzTokenParams":
        return cls(lz_token=obj.lz_token)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"lz_token": self.lz_token}

    def to_json(self) -> SetLzTokenParamsJSON:
        return {"lz_token": (None if self.lz_token is None else str(self.lz_token))}

    @classmethod
    def from_json(cls, obj: SetLzTokenParamsJSON) -> "SetLzTokenParams":
        return cls(
            lz_token=(
                None if obj["lz_token"] is None else Pubkey.from_string(obj["lz_token"])
            )
        )
