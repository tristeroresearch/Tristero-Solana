from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class InitNonceParamsJSON(typing.TypedDict):
    local_oapp: str
    remote_eid: int
    remote_oapp: list[int]


@dataclass
class InitNonceParams:
    layout: typing.ClassVar = borsh.CStruct(
        "local_oapp" / BorshPubkey,
        "remote_eid" / borsh.U32,
        "remote_oapp" / borsh.U8[32],
    )
    local_oapp: Pubkey
    remote_eid: int
    remote_oapp: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "InitNonceParams":
        return cls(
            local_oapp=obj.local_oapp,
            remote_eid=obj.remote_eid,
            remote_oapp=obj.remote_oapp,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "local_oapp": self.local_oapp,
            "remote_eid": self.remote_eid,
            "remote_oapp": self.remote_oapp,
        }

    def to_json(self) -> InitNonceParamsJSON:
        return {
            "local_oapp": str(self.local_oapp),
            "remote_eid": self.remote_eid,
            "remote_oapp": self.remote_oapp,
        }

    @classmethod
    def from_json(cls, obj: InitNonceParamsJSON) -> "InitNonceParams":
        return cls(
            local_oapp=Pubkey.from_string(obj["local_oapp"]),
            remote_eid=obj["remote_eid"],
            remote_oapp=obj["remote_oapp"],
        )
