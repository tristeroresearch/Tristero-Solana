from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class LzAccountJSON(typing.TypedDict):
    pubkey: str
    is_signer: bool
    is_writable: bool


@dataclass
class LzAccount:
    layout: typing.ClassVar = borsh.CStruct(
        "pubkey" / BorshPubkey, "is_signer" / borsh.Bool, "is_writable" / borsh.Bool
    )
    pubkey: Pubkey
    is_signer: bool
    is_writable: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "LzAccount":
        return cls(
            pubkey=obj.pubkey, is_signer=obj.is_signer, is_writable=obj.is_writable
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "pubkey": self.pubkey,
            "is_signer": self.is_signer,
            "is_writable": self.is_writable,
        }

    def to_json(self) -> LzAccountJSON:
        return {
            "pubkey": str(self.pubkey),
            "is_signer": self.is_signer,
            "is_writable": self.is_writable,
        }

    @classmethod
    def from_json(cls, obj: LzAccountJSON) -> "LzAccount":
        return cls(
            pubkey=Pubkey.from_string(obj["pubkey"]),
            is_signer=obj["is_signer"],
            is_writable=obj["is_writable"],
        )
