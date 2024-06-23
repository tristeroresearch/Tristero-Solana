from __future__ import annotations
from . import (
    message_lib_type,
)
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class RegisterLibraryParamsJSON(typing.TypedDict):
    lib_program: str
    lib_type: message_lib_type.MessageLibTypeJSON


@dataclass
class RegisterLibraryParams:
    layout: typing.ClassVar = borsh.CStruct(
        "lib_program" / BorshPubkey, "lib_type" / message_lib_type.layout
    )
    lib_program: Pubkey
    lib_type: message_lib_type.MessageLibTypeKind

    @classmethod
    def from_decoded(cls, obj: Container) -> "RegisterLibraryParams":
        return cls(
            lib_program=obj.lib_program,
            lib_type=message_lib_type.from_decoded(obj.lib_type),
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "lib_program": self.lib_program,
            "lib_type": self.lib_type.to_encodable(),
        }

    def to_json(self) -> RegisterLibraryParamsJSON:
        return {
            "lib_program": str(self.lib_program),
            "lib_type": self.lib_type.to_json(),
        }

    @classmethod
    def from_json(cls, obj: RegisterLibraryParamsJSON) -> "RegisterLibraryParams":
        return cls(
            lib_program=Pubkey.from_string(obj["lib_program"]),
            lib_type=message_lib_type.from_json(obj["lib_type"]),
        )
