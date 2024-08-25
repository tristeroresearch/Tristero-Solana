from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class RegisterTristeroOAppParamsJSON(typing.TypedDict):
    delegate: str
    admin_wallet: str
    payment_wallet: str


@dataclass
class RegisterTristeroOAppParams:
    layout: typing.ClassVar = borsh.CStruct(
        "delegate" / BorshPubkey,
        "admin_wallet" / BorshPubkey,
        "payment_wallet" / BorshPubkey,
    )
    delegate: Pubkey
    admin_wallet: Pubkey
    payment_wallet: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "RegisterTristeroOAppParams":
        return cls(
            delegate=obj.delegate,
            admin_wallet=obj.admin_wallet,
            payment_wallet=obj.payment_wallet,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "delegate": self.delegate,
            "admin_wallet": self.admin_wallet,
            "payment_wallet": self.payment_wallet,
        }

    def to_json(self) -> RegisterTristeroOAppParamsJSON:
        return {
            "delegate": str(self.delegate),
            "admin_wallet": str(self.admin_wallet),
            "payment_wallet": str(self.payment_wallet),
        }

    @classmethod
    def from_json(
        cls, obj: RegisterTristeroOAppParamsJSON
    ) -> "RegisterTristeroOAppParams":
        return cls(
            delegate=Pubkey.from_string(obj["delegate"]),
            admin_wallet=Pubkey.from_string(obj["admin_wallet"]),
            payment_wallet=Pubkey.from_string(obj["payment_wallet"]),
        )
