from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class ReceiveLibraryTimeoutJSON(typing.TypedDict):
    message_lib: str
    expiry: int


@dataclass
class ReceiveLibraryTimeout:
    layout: typing.ClassVar = borsh.CStruct(
        "message_lib" / BorshPubkey, "expiry" / borsh.U64
    )
    message_lib: Pubkey
    expiry: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "ReceiveLibraryTimeout":
        return cls(message_lib=obj.message_lib, expiry=obj.expiry)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"message_lib": self.message_lib, "expiry": self.expiry}

    def to_json(self) -> ReceiveLibraryTimeoutJSON:
        return {"message_lib": str(self.message_lib), "expiry": self.expiry}

    @classmethod
    def from_json(cls, obj: ReceiveLibraryTimeoutJSON) -> "ReceiveLibraryTimeout":
        return cls(
            message_lib=Pubkey.from_string(obj["message_lib"]), expiry=obj["expiry"]
        )
